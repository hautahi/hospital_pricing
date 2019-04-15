import os
import re
import pandas as pd
import numpy as np
from xlrd.biffh import XLRDError
from pandas.errors import ParserError

downloaded_files_loc = '../round1_scrape/downloaded_files'

def find_files():
    cwd = os.getcwd()  # Get the current working directory
    found_files = []  # List of files found
    empty_directories = []  # List of empty directories
    # Get all the directories in the downloaded_files folder
    directories = os.listdir(downloaded_files_loc)
    for directory in directories:
        # Check for files in each directory
        files = os.listdir(os.path.join(cwd, downloaded_files_loc, directory))
        for file in files:
            # Add file path for each file to found_files list
            found_files.append(os.path.join(cwd,downloaded_files_loc, directory, file))

        # If there are no files, then add directory to empty_directories list
        if len(files) == 0:
            empty_directories.append(directory)

    # Save the two lists as CSVs
    df_found = pd.DataFrame({'files': found_files})
    df_found.to_csv('found_files.csv', index=False)

    df_empty = pd.DataFrame({'directories': empty_directories})
    df_empty.to_csv('empty_directories.csv', index=False)


def get_column_name_bow(files_directory):
    bow = {}
    xml_count = 0
    directories = os.listdir(files_directory)
    for i, directory in enumerate(directories):
        # Check for files in each directory
        files = os.listdir(os.path.join(files_directory, directory))
        for file in files:
            if file == 'file_urls.csv':
                continue

            file_path = os.path.join(files_directory, directory, file)
            print(file_path)
            try:
                if file.endswith('.csv'):
                    df = pd.read_csv(file_path, encoding="ISO-8859-1", engine='python')
                    update_df_bow(df, bow)
                elif file.endswith('.xls') or file.endswith('.xlsx'):
                    sheets_dict = pd.read_excel(file_path, sheet_name=None)
                    for name, sheet in sheets_dict.items():
                        if not sheet.empty:
                            print(name)
                            update_df_bow(sheet, bow)
                elif file.endswith('.xml'):
                    xml_count += 1
                    continue
                else:
                    continue
            except (XLRDError, ParserError) as e:
                print(e)
                save_bow(bow)
            except:
                print('Error Index:', i)
                raise

    print(xml_count)
    save_bow(bow)


def update_df_bow(df, bow):
    df = find_header(df)

    columns = df.columns.values
    for column in columns:
        for word in re.split(r'\s|_', str(column).lower()):
            if word in bow:
                bow[word] += 1
            else:
                bow[word] = 1


def save_bow(bow):
    df_bow = pd.DataFrame({'words': list(bow.keys()), 'counts': list(bow.values())})
    df_bow.to_csv('column_bow.csv', index=False)


def is_cost_column(column):
    cost_keywords = ['price', 'charge', 'chg', 'cost', 'rate', 'fee', 'pricing', 'average', 'current']
    try:
        column_name = column.name.lower()
    except AttributeError:
        column_name = column.name

    confidence = 0
    for keyword in cost_keywords:
        if keyword in str(column_name):
            confidence += 1
            break

    # try:
    #     column.replace('[\$,]', '', regex=True).astype(float)
    #     confidence += 1
    # except (ValueError, AttributeError):
    #     pass

    number_cells = 0
    for cell in column.replace('[\$,]', '', regex=True):
        try:
            float(cell)
            number_cells += 1
        except ValueError:
            pass

    if number_cells / column.shape[0] > 0.9:
        confidence += 1

    return confidence


def check_columns(df):
    columns = df.columns.values
    confidence = 0
    for column in columns:
        try:
            col_confidence = is_cost_column(df[column])
        except:
            col_confidence = 0
        if col_confidence > confidence:
            confidence = col_confidence

    return confidence


def file_has_cost_column(df):
    confidence = check_columns(df)
    if confidence < 2:
        df = find_header(df)
        new_confidence = check_columns(df)
        if new_confidence > confidence:
            confidence = new_confidence

    return confidence


def files_with_cost(files_directory):
    result = {'file': [], 'sheet': [], 'confidence': []}
    directories = os.listdir(files_directory)
    pattern = re.compile(r'drg|cdm|charge.*(master)*|chg|pric(e|ing)|hourly.*rate|room.*rate', flags=re.IGNORECASE)
    for i, directory in enumerate(directories):
        # Check for files in each directory
        files = os.listdir(os.path.join(files_directory, directory))
        for file in files:
            if file == 'file_urls.csv':
                continue

            file_path = os.path.join(files_directory, directory, file)
            print(file_path)
            if pattern.search(file) is not None:
                result['file'].append(file_path)
                result['sheet'].append('')
                result['confidence'].append(2)
                continue

            try:
                if file.endswith('.csv'):
                    df = pd.read_csv(file_path, encoding="ISO-8859-1", engine='python').dropna(axis=0, how='all')
                    df = remove_nan_columns(df)
                    result['file'].append(file_path)
                    result['sheet'].append('')
                    result['confidence'].append(file_has_cost_column(df))
                elif file.endswith('.xls') or file.endswith('.xlsx'):
                    sheets_dict = pd.read_excel(file_path, sheet_name=None)
                    for name, sheet in sheets_dict.items():
                        if not sheet.empty:
                            sheet = remove_nan_columns(sheet)
                            result['file'].append(file_path)
                            result['sheet'].append(name)
                            result['confidence'].append(file_has_cost_column(sheet))
                else:
                    continue

            except (XLRDError, ParserError) as e:
                print(e)

    result = pd.DataFrame(result)
    result.to_csv('files_with_cost_column.csv', index=False)


def remove_nan_columns(df):
    drop_columns = []
    for column in df:
        nan_count = df[column].isna().sum()
        if nan_count / df.shape[0] > 0.75:
            drop_columns.append(column)

    return df.drop(columns=drop_columns)


def find_header(df):
    unnamed_count = 0
    for name in df.columns.values:
        try:
            if 'unnamed' in name.lower():
                unnamed_count += 1
        except AttributeError:
            pass

    if unnamed_count > 0:
        # This means that the top row might not be the column header
        lowest_nan_count = 10e9
        lowest_nan_idx = 0
        for idx, row in df.iterrows():
            nan_count = np.sum(row.isna())
            if nan_count < lowest_nan_count:
                lowest_nan_count = nan_count
                lowest_nan_idx = idx

        if lowest_nan_count < unnamed_count:
            df.columns = df.iloc[lowest_nan_idx]
            df = df.drop(df.index[list(range(lowest_nan_idx + 1))])

    try:
        df = df.loc[:, df.columns.notnull()]
    except KeyError:
        pass
    print(df.columns.values)
    return df


if __name__ == '__main__':
    # find_files()
    # get_column_name_bow('downloaded_files')
    files_with_cost(downloaded_files_loc)

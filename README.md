# hospital_pricing

## File Descriptions
- `1.scrape.py` takes the hospital list `Hospital_General_Information.csv` and grabs the top 3 pages in a google search, which are then stored as additional columns in `Hospital_General_Information_url.csv`

## AWS Setup Instructions
1. Setup instance on the AWS website
2. Login to AWS instance via: `ssh -i amazonkey.pem ec2-user@instance-address.amazonaws.com`
3. Setup AWS instance with: `sudo yum install python git tmux pip`.
4. The above setup sometimes messes up `pip`. If this is the case run `curl -O https://bootstrap.pypa.io/get-pip.py` and `python get-pip.py --user`.
5. Run `sudo pip install numpy pandas`
6. Install the [google search api](https://github.com/abenassi/Google-Search-API) package with `pip install git+https://github.com/abenassi/Google-Search-API`
7. Transfer file to instance: `scp -i amazonkey.pem file_name ec2-user@instance-address.amazonaws.com:`
8. Transfer folder to instance: `scp -i amazonkey.pem -r folder_name ec2-user@instance-address.amazonaws.com:`
9. Transfer files back to local machine: `scp -i amazonkey.pem -r ec2-user@instance-address.amazonaws.com: .`
10. Tip: Use `tmux` command before running a script to open a new screen. Transition back to main screen with `ctrl+b,d` and then back again using `tmux attach -d`. This allows you to log out of AWS while keeping a script running.

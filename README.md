# fork-repo-app using Github Oauth

Create an Oauth app in github
You will get the client_id and client_secret. Use it in later steps to set environment variables.

Install python3

clone the repo
git clone https://github.com/nitish21/fork-repo-app.git

cd fork-repo-app

env\Scripts\activate

# Set these environment variables

set CLIENT_ID=<your client id>
set CLIENT_SECRET=<your client secret>
set OAUTHLIB_INSECURE_TRANSPORT=1
set SECRET_KEY=<secret key>
set GITHUB_ACCOUNT=nitish21
set GITHUB_REPO=fork-repo-app

flask run

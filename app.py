try:
    from flask import Flask,render_template,url_for,request,redirect, make_response, session
    import random
    import json
    import requests
    from time import time
    from random import random
    from flask import Flask, render_template, make_response
    from flask_dance.contrib.github import make_github_blueprint, github
    from os import environ
except Exception as e:
    print("Some Modules are Missings {}".format(e))


app = Flask(__name__)

app.config["SECRET_KEY"]="cqwecewcewcewcwecwrec" # needed to keep the client-side sessions secure

# client_id, client_secret are obtained from github oath app
# These should be passed as environment variables from docker container
# SECRET_KEY should also be passed a environment variables


github_blueprint = make_github_blueprint(client_id=environ.get('CLIENT_ID'),
                                         client_secret=environ.get('CLIENT_SECRET'),
                                         scope='repo')

app.register_blueprint(github_blueprint, url_prefix='/github_login')


@app.route('/',methods=['GET'])
def github_login():

    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()

            repos_info = github.get('/user/repos')
            repos_info_json = repos_info.json()

            repo_names = []
            for repo in repos_info_json:
                repo_names.append(repo.get('full_name'))

            return render_template('index.html', loginName=account_info_json.get('login'), existing_repos=repo_names)


@app.route('/fork',methods=['GET'])
def fork():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        repos_info = github.get('/user/repos')
        repos_info_list = repos_info.json()
        repo_ids = []
        for repo in repos_info_list:
            repo_ids.append(repo.get('id'))

        forkResponse = github.post('repos/{}/{}/forks'.format(environ.get('GITHUB_ACCOUNT'), environ.get('GITHUB_REPO')))
        if forkResponse.json().get('id') in repo_ids:
            return 'Fork already exists'
        else:
            return 'Fork created successfully. Check here : {}'.format(forkResponse.json().get('html_url'))

    return '<h1>Request failed!</h1>'


@app.route('/logout', methods=['GET'])
def github_logout():
    del app.blueprints['github'].token
    session.clear()
    return redirect(url_for('github.login'))

if __name__ == "__main__":
    app.run(debug=True)
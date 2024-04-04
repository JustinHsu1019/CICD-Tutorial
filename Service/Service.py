from flask import Flask, request, abort
import git
import requests
import configparser

app = Flask(__name__)

@app.route('/')
def main_update():
    return "Service is ready!"

@app.route('/git_update', methods=['POST'])
def git_update():
    config_path = '/home/justincicd/CICD-First-Try/Service/config.ini'

    config = configparser.ConfigParser()
    config.read(config_path)

    token_header = request.headers.get('Authorization')
    if not token_header:
        abort(403, "未提供有效的 API Token")

    if token_header != "Token " + config['pythonanywhere']['github_secret']:
        abort(403, "提供錯誤的 API Token")

    pythonanywhere_username = config['pythonanywhere']['username']
    pythonanywhere_api_token = config['pythonanywhere']['api_token']
    domain_name = config['pythonanywhere']['domain_name']

    repo_path = './CICD-First-Try'

    repo = git.Repo(repo_path)
    origin = repo.remotes.origin
    origin.fetch()
    repo.git.reset('--hard', 'origin/master')

    response = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{pythonanywhere_username}/webapps/{domain_name}/reload/',
        headers={'Authorization': f'Token {pythonanywhere_api_token}'}
    )

    if response.status_code == 200:
        return "Updated Service from Git and reloaded PythonAnywhere web app", 200
    else:
        return f'Failed to update Service from Git and reload PythonAnywhere web app. Status code: {response.status_code}', 500

if __name__ == '__main__':
    app.run(threaded=True, debug=True)

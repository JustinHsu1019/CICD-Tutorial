from flask import Flask
import git
import requests
import configparser

app = Flask(__name__)

@app.route('/')
def main_update():
    return "Service is ready TWTWTWTW"

@app.route('/git_update', methods=['POST'])
def git_update():
    config_path = '/home/justincicd/CICD-First-Try/Service/config.ini'

    config = configparser.ConfigParser()
    config.read(config_path)

    pythonanywhere_username = config['pythonanywhere']['username']
    pythonanywhere_api_token = config['pythonanywhere']['api_token']
    domain_name = config['pythonanywhere']['domain_name']
    
    repo_path = './CICD-First-Try'
    file_to_update = 'Service/Service.py'

    repo = git.Repo(repo_path)
    origin = repo.remotes.origin
    origin.fetch()
    repo.git.checkout('origin/master', '--', file_to_update)

    response = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{pythonanywhere_username}/webapps/{domain_name}/reload/',
        headers={'Authorization': f'Token {pythonanywhere_api_token}'}
    )

    if response.status_code == 200:
        return "Force-updated specific file from Git and reloaded PythonAnywhere web app", 200
    else:
        return f'Failed to reload PythonAnywhere web app. Status code: {response.status_code}', 500

if __name__ == '__main__':
    app.run(threaded=True, debug=True)

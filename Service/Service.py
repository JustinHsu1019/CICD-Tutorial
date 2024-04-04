from flask import Flask, request, abort
import git
import requests
import configparser
import hmac
import hashlib

app = Flask(__name__)

@app.route('/')
def main_update():
    return "Service is ready JUSTTEST"

def verify_signature(payload_body, secret_token, signature_header):
    """驗證從GitHub發送的請求，確認其SHA256簽名的有效性。

    如果未經授權，則拋出403錯誤。

    Args:
        payload_body: 請求的原始體，用於驗證（request.data）。
        secret_token: GitHub應用的webhook秘鑰。
        signature_header: 從GitHub收到的x-hub-signature-256頭信息。
    """
    if not signature_header:
        abort(403, "X-Hub-Signature-256頭信息缺失！")

    signature = signature_header.split('=')[1]

    hmac_gen = hmac.new(secret_token, payload_body, hashlib.sha256)
    expected_signature = "sha256=" + hmac_gen.hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        abort(403, "請求簽名不匹配！")

@app.route('/git_update', methods=['POST'])
def git_update():
    config_path = '/home/justincicd/CICD-First-Try/Service/config.ini'

    config = configparser.ConfigParser()
    config.read(config_path)

    secret_token = config['pythonanywhere']['github_secret'].encode('utf-8')

    signature_header = request.headers.get('X-Hub-Signature-256')
    verify_signature(request.data, secret_token, signature_header)

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
        return "Updated Service from Git and reloaded PythonAnywhere web app", 200
    else:
        return f'Failed to update Service from Git and reload PythonAnywhere web app. Status code: {response.status_code}', 500

if __name__ == '__main__':
    app.run(threaded=True, debug=True)

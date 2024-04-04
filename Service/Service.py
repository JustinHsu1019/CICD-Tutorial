from flask import Flask
import git

app = Flask(__name__)

@app.route('/')
def main_update():
    return "Service is ready XDXDXD"

@app.route('/git_update', methods=['POST'])
def git_update():
    repo_path = './CICD-First-Try'
    repo = git.Repo(repo_path)
    origin = repo.remotes.origin

    origin.fetch()

    file_to_update = 'Service/Service.py'

    repo.git.checkout('origin/master', '--', file_to_update)

    return "Force-updated specific file from Git", 200

if __name__ == '__main__':
    app.run(debug=True)

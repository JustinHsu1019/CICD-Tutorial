from flask import Flask
import git

app = Flask(__name__)

@app.route('/')
def main_update():
    return "Service is ready"

@app.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./CICD-First-Try')
    origin = repo.remotes.origin
    repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
    origin.pull()
    return "Pulled", 200

if __name__ == '__main__':
    app.run(debug=True)
# 0405
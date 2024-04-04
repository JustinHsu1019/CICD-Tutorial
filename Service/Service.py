from flask import Flask

app = Flask(__name__)

@app.route('/')
def git_update():
    return "Service is ready"

if __name__ == '__main__':
    app.run(debug=True)

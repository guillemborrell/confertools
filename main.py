import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('main.html')

@app.route('/<folder>/<file>')
def serve_static(folder, file):
    with open(os.path.join(os.curdir, 'static', folder, file)) as f:
        return f.read()

if __name__ == '__main__':
    app.debug = True
    app.run()

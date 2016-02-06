import os
import json
from flask import Flask, render_template
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('main.html')

@app.route('/time/<timezone>')
def time(timezone):
    date_object =  datetime.utcnow()
    parsed_date = {'minute': date_object.minute,
                   'hour':   date_object.hour,
                   'second': date_object.second}
    return json.dumps(parsed_date)

@app.route('/<folder>/<file>')
def serve_static(folder, file):
    with open(os.path.join(os.curdir, 'static', folder, file)) as f:
        return f.read()

if __name__ == '__main__':
    app.debug = True
    app.run()

from flask_cors import cross_origin
from flask import render_template
from app import app


@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='*')
def index():
    return render_template('index.html')


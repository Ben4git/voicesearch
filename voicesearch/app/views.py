import json
import requests
from flask_cors import CORS, cross_origin
from flask import render_template, request
from app import app


@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='*')
def index():
    return render_template('index.html')


import json
import requests
from flask import render_template, request
from app import app

ELASTIC_BASE = 'http://www-explorer.pthor.ch/elastic/all_products_spryker_read/_search?q={}&size=10'


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    result = {}
    if request.method == "POST":
        try:
            text = request.form['text']
            s_text = generate_elastic_url(text)
            s = requests.get(s_text)
            s_message = json.loads(s.content)
            s_table = s_message['hits']['hits']

            def extract_product_info(hit):
                return {'name': hit['_source']['de_CH']['name'],
                        'image': hit['_source']['images']['lowres'][0]}

            result = map(extract_product_info, s_table)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('index.html', errors=errors, result=result)

def generate_elastic_url(search):
    return ELASTIC_BASE.format(search)

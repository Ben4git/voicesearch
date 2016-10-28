import json
import requests
from flask_cors import CORS, cross_origin
from flask import render_template, request
from app import app

ELASTIC_BASE = 'http://www-explorer.pthor.ch/elastic/all_products_spryker_read/_search?q={}&size=12'


@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='*')
def index():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            print 'start'
            text = request.form['text']
            s_text = generate_elastic_url(text)
            s = requests.get(s_text)
            s_message = json.loads(s.content)
            s_table = s_message['hits']['hits']
            print s_message
            def extract_product_info(hit):
                return {'name': hit['_source']['de_CH']['name'],
                        'image': hit['_source']['images']['lowres'][0],
                        'url': hit['_source']['de_CH']['url'],
                        'price': ((hit['_source']['min_price'])),
                        'merchant': hit['_source']['merchants']
                        }


            results = map(extract_product_info, s_table)
        except:
            print 'error, cant connect'
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )

    return render_template('index.html', errors=errors, results=results)

def generate_elastic_url(search):
    return ELASTIC_BASE.format(search)

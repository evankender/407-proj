from selectorlib import Extractor
import requests
import json
from time import sleep
import flask
from flask import Flask, redirect, url_for, request, render_template
import logging
import os
from flask_restful import Resource, Api
from bson import json_util

app = flask.Flask(__name__)
api = Api(app)

e = Extractor.from_yaml_file('selectors.yml')

class getPageData(Resource):
    def get(self, type="json"):
        if request.args.get('url') is not None:
            app.logger.info(request.args.get('url'))

api.add_resource(listAll, '/url')
api.add_resource(listAll, '/url/<type>', endpoint="url")

def scrape(url):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)


if __name__ == "__main__":
    print("Opening for global access on port {}".format(5000))
    app.run(port=5000, host="0.0.0.0")

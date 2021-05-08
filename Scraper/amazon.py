from selectorlib import Extractor
import requests
import json
from time import sleep
import flask
from flask import Flask, redirect, url_for, request, render_template
import logging
import os
from flask_restful import Resource, Api

app = flask.Flask(__name__)
api = Api(app)

amazonProduct = Extractor.from_yaml_file('amazonProduct.yml')

class getPageData(Resource):
    def get(self, type="json"):
        if request.args.get('url') is not None:
            return flask.make_response(scrape(request.args.get('url')))

api.add_resource(getPageData, '/getPageData')
api.add_resource(getPageData, '/getPageData/<type>', endpoint="getPageData")

def scrape(url):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Ch0.0.0rome/51.0.2704.64 Safari/537.36',
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
    return amazonProduct.extract(r.text)


if __name__ == "__main__":
    print("Opening for global access on port {}".format(5000))
    app.run(port=5000, host="0.0.0.0")

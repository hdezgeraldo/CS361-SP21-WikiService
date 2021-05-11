# Name: Geraldo Hernandez Garcia
# Description: Simple Wikipedia Scrapper Service
# Course: CS361 Spring 2021
#
# Google App Engine Flexible Template derived from:
# https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/flexible
# Copyright 2015 Google Inc. All Rights Reserved.

# [START gae_flex_quickstart]
import logging
import requests
import json
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    # Obtain POST request
    data = request.json

    # Dump JSON object to variable
    json_str = json.dumps(data)

    # Load JSON to string
    resp = json.loads(json_str)

    # Concatenate result to a string
    siteURL = 'https://en.wikipedia.org/wiki/' + str((resp['site']))

    # Start request to Wikipedia page
    source = requests.get(siteURL).text
    soup = BeautifulSoup(source, 'lxml')

    # Search for the first poster image in wikipedia article and get its source
    if soup.find('td', class_='infobox-image') :
        infobox = soup.find('td', class_='infobox-image')
        imagebox = infobox.find('img')
        imageSource = imagebox['src']

        results = {
            "imageURL": imageSource
        }
    else:
        results = "Wikipedia article not found"

    # Return data in JSON format
    return results


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]

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
from flask import Flask, request, abort, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

# Name: wikiScrapper
# @Param: string - HTTP URL string
# Description: This function will scrap a valid Wikipedia article for
# the first image
def wikiScrapper(string):
    # Hold expected URL string to only run with Wiki links
    wikiValidator = "https://en.wikipedia.org/wiki/"

    if string.startswith(wikiValidator):

        source = requests.get(string).text
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

    else:
        return "<h1>this isn't a valid WIKI link</h1>"

# Homepage: shows API instructions
@app.route('/')
def index():
    return render_template('index.html')

# Image Scrapper: Holds image scrapper app
@app.route('/image-scrapper', methods=['GET', 'POST'])
def my_request():
    # Verify if GET response
    if request.method == 'GET':
        # Get all URL parameters
        URLparams = request.args.get('url', type=str)

        # Show user error page if incorrect URL parameters
        if not URLparams:
            abort(404)

        else:
            # run wikiScrapper program
            return wikiScrapper(URLparams)

    # Verify if POST response
    elif request.method == 'POST':
        # Obtain POST request
        data = request.json

        # Dump JSON object to variable
        json_str = json.dumps(data)

        # Load JSON to string
        resp = json.loads(json_str)

        # hold JSON string response
        userResponse = str((resp['url']))

        # run wikiScrapper program
        return wikiScrapper(userResponse)


# Custom Error page
@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404


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
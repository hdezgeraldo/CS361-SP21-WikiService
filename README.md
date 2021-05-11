# CS361-SP21-WikiService

This is a simple Wikipedia Image Scraper Service using;

-   Python
-   Flask
-   Google App Engine

The template for my web app was derived from Google's Python Examples:
https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/flexible

## How it works

To submit a POST request:
` { "site": "The_Avengers_(2012_film)" }`

JSON Response:
`{ "imageURL": "//upload.wikimedia.org/wikipedia/en/8/8a/The_Avengers_%282012_film%29_poster.jpg" }`

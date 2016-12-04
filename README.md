# Multi User Blog
Multi user blog built using google app engine with webapp2

## Setup
* Install [Google App Engine SDK](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).
* [Sign Up for a Google App Engine Account](https://console.cloud.google.com/appengine).
* Create a new project in [Google’s Developer Console](https://console.cloud.google.com/) using a unique name.
* Follow the [App Engine Quickstart](https://cloud.google.com/appengine/docs/python/quickstart) to get a sample app up and running.

## Running blog locally
1. Clone this directory.
2. Since Python module **pytz** is used to consider timezone issues, it is required to install **pytz** into project's directory:
  * Create a directory to store third-party libraries <br>
    `mkdir lib`
  * Use pip (version 6 or later) with the -t flag to copy the libraries into the folder you created in the previous step.
    `pip install -t lib/ pytz`
3. You can then execute `dev_appserver.py .` in the directory to run a copy of the app on your own computer, and access it at http://localhost:8080/.

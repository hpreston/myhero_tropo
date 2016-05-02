from flask import Flask, request, Response
import requests, json, re

from tropo import Tropo

app = Flask(__name__)


app_headers = {}
app_headers["Content-type"] = "application/json"


@app.route('/', methods=["POST"])
def index():
    t = Tropo()
    t.say("Welcome to Tropo!")
    return t.RenderJson()


if __name__ == '__main__':
    from argparse import ArgumentParser
    import os, sys
    from pprint import pprint

    # Setup and parse command line arguments
    parser = ArgumentParser("MyHero Spark Interaction Bot")
    parser.add_argument(
        "-a", "--app", help="Address of app server", required=False
    )
    parser.add_argument(
        "-k", "--appkey", help="App Server Authentication Key Used in API Calls", required=False
    )
    parser.add_argument(
        "-s", "--secret", help="Key Expected in API Calls", required=False
    )

    args = parser.parse_args()

    app_server = args.app
    # print "Arg App: " + str(app_server)
    if (app_server == None):
        app_server = os.getenv("myhero_app_server")
        # print "Env App: " + str(app_server)
        if (app_server == None):
            get_app_server = raw_input("What is the app server address? ")
            # print "Input App: " + str(get_app_server)
            app_server = get_app_server
    # print "App Server: " + app_server
    sys.stderr.write("App Server: " + app_server + "\n")

    app_key = args.appkey
    # print "Arg App Key: " + str(app_key)
    if (app_key == None):
        app_key = os.getenv("myhero_app_key")
        # print "Env App Key: " + str(app_key)
        if (app_key == None):
            get_app_key = raw_input("What is the app server authentication key? ")
            # print "Input App Key: " + str(get_app_key)
            app_key = get_app_key
    # print "App Server Key: " + app_key
    sys.stderr.write("App Server Key: " + app_key + "\n")

    # secret_key = args.secret
    # if (secret_key == None):
    #     secret_key = os.getenv("myhero_spark_bot_secret")
    #     if (secret_key == None):
    #         get_secret_key = raw_input("What is the Authorization Key to Require? ")
    #         secret_key = get_secret_key
    # sys.stderr.write("Secret Key: " + secret_key + "\n")


    # Set Authorization Details for external requests
    app_headers["key"] = app_key

    app.run(debug=True, host='0.0.0.0', port=int("5000"))

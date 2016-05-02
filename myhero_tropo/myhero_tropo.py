from flask import Flask, request, Response
import requests, json, re
from itty import *

from tropo import Tropo, Session

# app = Flask(__name__)


app_headers = {}
app_headers["Content-type"] = "application/json"


# @app.route('/', methods=["POST"])
@post('/index.json')
def index(request):
    t = Tropo()

    # s = Session(request.get_json(force=True))
    s = Session(request.body)
    message = s.initialText
    # print("Initial Text: " + initialText)


    # Check if message contains word "results" and if so send results
    if message["text"].lower().find("results") > -1:
        results = get_results()
        reply = "The current standings are\n"
        for result in results:
            reply += "  - %s has %s votes.\n" % (result[0], result[1])
    # Check if message contains word "options" and if so send options
    elif message["text"].lower().find("options") > -1:
        options = get_options()
        reply = "The options are... \n"
        for option in options:
            reply += "  - %s \n" % (option)
    # Check if message contains word "vote" and if so start a voting session
    # elif message["text"].lower().find("vote") > -1:
    #     reply = "Let's vote!  Look for a new message from me so you can place a secure vote!"
    #     start_vote_session(message["personEmail"])
    # Check if message contains phrase "add email" and if so add user to room
    # If nothing matches, send instructions
    else:
        # Reply back to message
        reply = "Hello, welcome to the MyHero Demo Room.\n" \
                "To find out current status of voting, ask 'What are the results?'\n" \
                "To find out the possible options, ask 'What are the options?\n" \
                '''To place a vote, say "I'd like to vote" to start a private voting session.'''



    # t.say(["Really, it's that easy." + message])
    t.say([reply])
    return t.RenderJson()

# Utilities to interact with the MyHero-App Server
def get_results():
    u = app_server + "/results"
    page = requests.get(u, headers = app_headers)
    tally = page.json()
    tally = sorted(tally.items(), key = lambda (k,v): v, reverse=True)
    return tally

def get_options():
    u = app_server + "/options"
    page = requests.get(u, headers=app_headers)
    options = page.json()["options"]
    return options

def place_vote(vote):
    u = app_server + "/vote/" + vote
    page = requests.post(u, headers=app_headers)
    return page.json()



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

    # app.run(debug=True, host='0.0.0.0', port=int("5000"))
    run_itty(server='wsgiref', host='0.0.0.0', port=5000)

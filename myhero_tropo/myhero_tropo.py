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
    if message.lower().find("results") > -1:
        results = get_results()
        reply = ["The current standings are"]
        for result in results:
            reply.append("  - %s has %s votes.\n" % (result[0], result[1]))
    # Check if message contains word "options" and if so send options
    elif message.lower().find("options") > -1:
        options = get_options()
        reply = ["The options are..."]
        for option in options:
            reply.append("  - %s \n" % (option))
    # Check if message contains word "vote" and if so start a voting session
    elif message.lower().find("vote") > -1:
        # reply = "Let's vote!  Look for a new message from me so you can place a secure vote!"
        reply = [process_incoming_message(message)]
    # If nothing matches, send instructions
    else:
        # Reply back to message
        # reply = "Hello, welcome to the MyHero Demo Room.\n" \
        #         "To find out current status of voting, ask 'What are the results?'\n" \
        #         "To find out the possible options, ask 'What are the options?\n" \
        #         '''To place a vote, simply type the name of your favorite Super Hero and the word "vote".'''
        reply = ["Hello, welcome to the MyHero Demo Room." ,
                "To find out current status of voting, ask 'What are the results?'",
                "To find out the possible options, ask 'What are the options?",
                '''To place a vote, simply type the name of your favorite Super Hero and the word "vote".''']

    # t.say(["Really, it's that easy." + message])
    t.say(reply)
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

# Figure out who to vote for
def process_incoming_message(message):
    # What to do...
    # 1.  Get Possible Options
    # 2.  See if the message contains one of the options
    # 3.  Cast vote for option
    # 4.  Thank the user for their vote
    # 5.  Delete Webhook

    options = get_options()
    chosen_hero = ""
    for option in options:
        if message.lower().find(option.lower()) > -1:
            pprint("Found a vote for: " + option)
            chosen_hero = option
            break

    # Cast Vote
    if chosen_hero != "":
        vote = place_vote(chosen_hero)
        msg = "Thanks for your vote for %s.  Your vote has been recorded and this ends this voting session." % (chosen_hero)
    else:
        msg = "I didn't understand your vote, please type the name of your chosen hero exactly as listed on the ballot.  "
    return msg


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

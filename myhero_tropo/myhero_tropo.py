#! /usr/bin/python
'''
    Tropo WebAPI Endpoint for Simple Superhero Voting Application

    This is a WebAPI Service for Cisco Tropo to respond to Text or Voice based
    interaction withe the MyHero Application.  Users can
    check current standings, list the available options, and place a vote.

    This is the an example Service for a basic microservice demo application.
    The application was designed to provide a simple demo for Cisco Mantl

    There are several pieces of information needed to run this application.  It is
    suggested to set them as OS Environment Variables.  Here is an example on how to
    set them:

    # Address and key for app server
    export myhero_app_server=http://myhero-app.mantl.domain.com
    export myhero_app_key=DemoAppKey
    export myhero_tropo_secret=DevTropo
    export myhero_tropo_user=tropouser
    export myhero_tropo_pass=tropopass
    export myhero_tropo_prefix=1419
    export myhero_tropo_url=http://localhost:5000



'''

__author__ = 'hapresto'

# Todo - Convert back to flask "json.dumps(page.json)"
# Todo - Add in Auth Code for API calls
# Todo - Setup Local Development Environment Details in README
# Todo - Add support for multiple phone numbers
# Todo - Add support for a prefix that isn't supported by Tropo being used, right now big error

# from flask import Flask, request, Response
import requests, json, re
from requests.auth import HTTPBasicAuth
from itty import *
from tropo import Tropo, Session

# app = Flask(__name__)

# Tropo API Details
tropo_host = "https://api.tropo.com/v1"
tropo_headers = {}
tropo_headers["Content-type"] = "application/json"

# MyHero APP Details
app_headers = {}
app_headers["Content-type"] = "application/json"


# @app.route('/', methods=["POST"])
@post('/')
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

@get('/application')
def display_tropo_application(request):
    return json.dumps(demoapp)

@get('/application/number')
def display_tropo_application_number(request):
    return json.dumps(demoappnumber)

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

# Tropo Utilities
def get_applications():
    tropo_u = tropo_host + "/applications"
    page = requests.get(tropo_u, headers = tropo_headers, auth=HTTPBasicAuth(tropo_user, tropo_pass))
    applications = page.json()
    return applications

def get_application_addresses(application):
    tropo_u = tropo_host + "/applications/%s/addresses" % (application["id"])
    page = requests.get(tropo_u, headers = tropo_headers, auth=HTTPBasicAuth(tropo_user, tropo_pass))
    addresses = page.json()
    return addresses

def create_application(appname, appurl):
    data = {
    "name":appname,
    "voiceUrl":appurl,
    "messagingUrl":appurl,
    "platform":"webapi",
    "partition":"staging"
    }

    tropo_u = tropo_host + "/applications"
    page = requests.post(tropo_u, headers = tropo_headers, auth=HTTPBasicAuth(tropo_user, tropo_pass), json=data)
    appurl = page.json()["href"]

    page = requests.get(appurl, headers = tropo_headers, auth=HTTPBasicAuth(tropo_user, tropo_pass))
    app = page.json()
    return app

def set_application_url(application, appurl):
    data = {
    "name":application["name"],
    "voiceUrl":appurl,
    "messagingUrl":appurl,
    "platform":"webapi",
    "partition":"staging"
    }

    tropo_u = tropo_host + "/applications/%s" % (application["id"])
    page = requests.put(tropo_u, headers = tropo_headers, auth=HTTPBasicAuth(tropo_user, tropo_pass), json=data)
    appurl = page.json()["href"]

    page = requests.get(appurl, headers = tropo_headers, auth=HTTPBasicAuth(tropo_user, tropo_pass))
    app = page.json()
    return app

def add_number(application, prefix):
    data = {
    "type":"number",
    "prefix":prefix
    }

    tropo_u = tropo_host + "/applications/%s/addresses" % (application["id"])
    page = requests.post(tropo_u, headers = tropo_headers, auth=HTTPBasicAuth(tropo_user, tropo_pass), json=data)
    print page
    addressurl = page.json()["href"]

    page = requests.get(addressurl, headers = tropo_headers, auth=HTTPBasicAuth(tropo_user, tropo_pass))
    address = page.json()
    return address

# Standard Utility
def valid_request_check(request):
    try:
        if request.headers["key"] == secret_key:
            return (True, "")
        else:
            error = {"Error": "Invalid Key Provided."}
            print error
            status = 401
            resp = Response(json.dumps(error), content_type='application/json', status=status)
            return (False, resp)
    except KeyError:
        error = {"Error": "Method requires authorization key."}
        print error
        status = 400
        resp = Response(json.dumps(error), content_type='application/json', status=status)
        return (False, resp)



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
    parser.add_argument(
        "-t", "--tropouser", help="Tropo Username", required=False
    )
    parser.add_argument(
        "-p", "--tropopass", help="Tropo Password", required=False
    )
    parser.add_argument(
        "--tropoprefix", help="Tropo Number Prefix", required=False
    )
    parser.add_argument(
        "--tropourl", help="Local Address for Tropo App URL", required=False
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

    secret_key = args.secret
    if (secret_key == None):
        secret_key = os.getenv("myhero_tropo_secret")
        if (secret_key == None):
            get_secret_key = raw_input("What is the Authorization Key to Require? ")
            secret_key = get_secret_key
    sys.stderr.write("Secret Key: " + secret_key + "\n")

    tropo_user = args.tropouser
    if (tropo_user == None):
        tropo_user = os.getenv("myhero_tropo_user")
        if (tropo_user == None):
            get_tropo_user = raw_input("What is the Tropo Username? ")
            tropo_user = get_tropo_user
    sys.stderr.write("Tropo User: " + tropo_user + "\n")

    tropo_prefix = args.tropoprefix
    if (tropo_prefix == None):
        tropo_prefix = os.getenv("myhero_tropo_prefix")
        if (tropo_prefix == None):
            get_tropo_prefix = raw_input("What is the Tropo Prefix? ")
            tropo_prefix = get_tropo_prefix
    sys.stderr.write("Tropo Prefix: " + tropo_prefix + "\n")

    tropo_pass = args.tropopass
    if (tropo_pass == None):
        tropo_pass = os.getenv("myhero_tropo_pass")
        if (tropo_pass == None):
            get_tropo_pass = raw_input("What is the Tropo Password? ")
            tropo_pass = get_tropo_pass
    sys.stderr.write("Tropo Pass: " + tropo_pass + "\n")

    tropo_url = args.tropourl
    if (tropo_url == None):
        tropo_url = os.getenv("myhero_tropo_url")
        if (tropo_url == None):
            get_tropo_url = raw_input("What is the Local Tropo App URL? ")
            tropo_url = get_tropo_url
    sys.stderr.write("Tropo URL: " + tropo_url + "\n")


    # Set Authorization Details for external requests
    app_headers["key"] = app_key

    # Find if Tropo Application "myherodemo" already exists
    # If not, create it
    # If exists, verify has correct url and a number in the correct prefix
    tropo_applications = get_applications()

    demoappid = ""
    demoapp = {}
    demoappnumber = ""
    demoappprefix = ""

    for app in tropo_applications:
        if app["name"] == "myherodemo":
            # pprint("Found Demo App")
            demoappid = app["id"]
            demoapp = app
            if demoapp["messagingUrl"] != tropo_url:
                pprint("Updated App URLs")
                demoapp = set_application_url(demoapp, tropo_url)

    if demoappid == "":
        pprint("Creating Tropo App")
        demoapp = create_application("myherodemo", tropo_url)
        demoappid = demoapp["id"]
        # pprint(demoapp)

    pprint("Tropo App: %s - %s" % (demoappid, demoapp["name"]))
    # pprint(demoapp)

    addresses = get_application_addresses(demoapp)
    for address in addresses:
        if address["type"] == "number" and address["prefix"] == tropo_prefix:
            # pprint("Found Address")
            demoappnumber = address["number"]
            demoappprefix = address["prefix"]

    if demoappnumber == "":
        pprint ("Creating Tropo Number")
        address = add_number(demoapp, tropo_prefix)
        demoappnumber = address["number"]
        demoappprefix = address["prefix"]

    pprint("Tropo Number: " + demoappnumber)

    # app.run(debug=True, host='0.0.0.0', port=int("5000"))
    run_itty(server='wsgiref', host='0.0.0.0', port=5000)

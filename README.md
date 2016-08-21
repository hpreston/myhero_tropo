# MyHero Tropo WebAPI Interface

This is a Tropo WebAPI for a basic microservice demo application.
This provides an interactive text and voice service for a voting system where users can vote for their favorite movie superhero.

Details on deploying the entire demo to a Mantl cluster can be found at

* MyHero Demo - [hpreston/myhero_demo](https://github.com/hpreston/myhero_demo)

The application was designed to provide a simple demo for Cisco Mantl.  It is written as a simple Python Flask application and deployed as a docker container.

Other services are:

* Data - [hpreston/myhero_data](https://github.com/hpreston/myhero_data)
* App - [hpreston/myhero_app](https://github.com/hpreston/myhero_app)
* Web - [hpreston/myhero_web](https://github.com/hpreston/myhero_web)
* UI - [hpreston/myhero_ui](https://github.com/hpreston/myhero_ui)
* Ernst - [hpreston/myhero_ernst](https://github.com/hpreston/myhero_ernst)
  * Optional Service used along with an MQTT server when App is in "queue" mode
* Spark Bot - [hpreston/myhero_spark](https://github.com/hpreston/myhero_spark)
  * Optional Service that allows voting through IM/Chat with a Cisco Spark Bot
* Tropo App - [hpreston/myhero_tropo](https://github.com/hpreston/myhero_tropo)
  * Optional Service that allows voting through TXT/SMS messaging


The docker containers are available at

* Data - [hpreston/myhero_data](https://hub.docker.com/r/hpreston/myhero_data)
* App - [hpreston/myhero_app](https://hub.docker.com/r/hpreston/myhero_app)
* Web - [hpreston/myhero_web](https://hub.docker.com/r/hpreston/myhero_web)
* UI - [hpreston/myhero_ui](https://hub.docker.com/r/hpreston/myhero_ui)
* Ernst - [hpreston/myhero_ernst](https://hub.docker.com/r/hpreston/myhero_ernst)
  * Optional Service used along with an MQTT server when App is in "queue" mode
* Spark Bot - [hpreston/myhero_spark](https://hub.docker.com/r/hpreston/myhero_spark)
  * Optional Service that allows voting through IM/Chat with a Cisco Spark Bot
* Tropo App - [hpreston/myhero_tropo](https://hub.docker.com/r/hpreston/myhero_tropo)
  * Optional Service that allows voting through TXT/SMS messaging

## Cisco Tropo Account Requirement
In order to use this service, you will need a Cisco Tropo Account deploy the service.

Creating an account is free and only requires a working email account.  Visit [http://www.tropo.com](http://www.tropo.com) to signup for an account.

Developer usage of Tropo is also free and information is available at [http://www.tropo.com](http://www.tropo.com).

In order to build the Tropo Application, this application needs the Username and Password for your Tropo Account.


## Basic Application Details
**EDIT NEEDED**


Required

* requests
* tropo-webapi-python
* flask
* argparse
* itty


# Environment Installation

    pip install -r requirements.txt

# Basic Usage

In order to run, the service needs several pieces of information to be provided:

* App Server Address
* App Server Authentication Key to Use
* Secret Key to require for local API Calls
* Tropo Username
* Tropo Password
* Tropo Phone Number Prefix
* Tropo Service URL

These details can be provided in one of three ways.

* As a command line argument
  - `python myhero_tropo/myhero_tropo.py --app "http://myhero-app.server.com" --appkey "APP AUTH KEY" --secret "TROPO KEY" --tropouser "tuser" --tropopassword "tpass" --tropoprefix "1419" --tropourl "http://localhost:5000" `
* As environment variables
  - `export myhero_app_server=http://myhero-app.server.com`
  - `export myhero_app_key=APP AUTH KEY`
  - `export myhero_tropo_secret=TROPO KEY`
  - `export myhero_tropo_user=tuser`
  - `export myhero_tropo_pass=tpass`
  - `export myhero_tropo_prefix=1419`
  - `export myhero_tropo_url=http://localhost:5000`
  - `python myhero_tropo/myhero_tropo.py`

* As raw input when the application is run
  - `python myhero_tropo/myhero_tropo.py`
  - `What is the app server address? http://myhero-app.server.com`
  - `App Server Key: APP AUTH KEY`

A command line argument overrides an environment variable, and raw input is only used if neither of the other two options provide needed details.

# Accessing

* At first run, the tropo service will create a new Tropo Applciation called "myherodemo".  You can use log into the Tropo interface to verify this application and details.
* The service has API endpoints to return details about the Tropo Application.
  * Execute this curl command to get details on the Tropo Application
  * `curl -H "key: TROPO KEY" http://localhost:5000/application`
  * Execute this curl command to get the phone number assigned to the Tropo Application
  * `curl -H "key: TROPO KEY" http://localhost:5000/application/number`


## Interacting with the Tropo Application
The Tropo Application is a very simple interface that is designed to make it intuitive to use.  Once in the room, simply say "hello", "help" (or anything else) to have the bot reply back with some instructions on how to access the features.

Start by sending a TXT (SMS) message to the phone number assigned to the application.

* This number can be found in the Tropo Web Portal or with this command
  * `curl -H "key: SecureTropo" http://myhero-tropo.$MANTL_DOMAIN/application/number`

The Application is designed to look for key words to act on, and provide the basic help message for anything else.  The key words are:

* options
  * return a list of the current available options to vote on
* results
  * list the current status of voting results
* vote **Option**
  * register a vote for the identified option

## REST APIs

# /

The main service API is at the root of the applciation and is what is used by the Tropo Application.  

# /hello/:phonenumber 

There is an API call that can be leveraged to have the Tropo Bot initiate an SMS session with a user.  This API responds to GET requests and then will send a SMS message to the phone number provided.  

Example usage

```
curl http://myhero-tropo.domain.local/hello/5551234567
```

# /health 

This is an API call that can be used to test if the Tropo Bot service is functioning properly.
  
```
curl -v http://myhero-tropo.domain.local/health 

*   Trying...
* Connected to myhero-tropo.domain.local (x.x.x.x)
> GET /health HTTP/1.1
> Host: myhero-tropo.domain.local
> User-Agent: curl/7.43.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Connection: close
< 
* Closing connection 0
Service up. 
```

# Local Development with Vagrant

I've included the configuration files needed to do local development with Vagrant in the repo.  Vagrant will still use Docker for local development and is configured to spin up a CentOS7 host VM for running the container.

Before running `vagrant up` you will need to finish the Vagrant file configuration by adding the Tropo Username and Password to the environment variables used by the container.  You will also need to change the URL that the Tropo service will be available at when in production.  You can optionally change the prefix that the myHero_tropo service will use to create a number for the application.

To do this:

* Make a copy of Vagrantfile.sample to use
  * `cp Vagrantfile.sample Vagrantfile`
* Edit `Vagrantfile` and add your details where indicated
  * `vim Vagrantfile`
  * Change the values for
    * `"myhero_tropo_user" => "TROPOUSER",`
    * `"myhero_tropo_pass" => "TROPOPASSWORD",`
    * `"myhero_tropo_prefix" => "1408",`
    * `"myhero_tropo_url" => "http://myhero-tropo.TRAEFIKDOMAIN",`

To start local development run:
* `vagrant up`
  - You may need to run this twice.  The first time to start the docker host, and the second to start the container.
* Now you can interact with the API or interface at localhost:15005 (configured in Vagrantfile and Vagrantfile.host)
  - example:  from your local machine `curl -H "key: DevTropo" http://localhost:15005/application/numbers` to return the list of phone numbers available for this applciation
  - Environment Variables are configured in Vagrantfile for development

Tropo makes building and developing applications very straightforward, but there is a couple of aspects of the nature of the service that add a little extra complexity.  For this service, I opted to use the WebAPI to build an independent Microservice rather than let Tropo host the application code and use their ScriptingAPI.  In this model, the Tropo Cloud Service sends a REST API call to the registered "messagingUrl" for the application.  This URL needs to be accessible from the public internet hosted Tropo cloud.  This is typically not practical for a development laptop and a workaround is needed.

One way to get started is to leverage [Requestb.in](http://requestb.in), which is a free service that will provide you a publicly available URL to use during testing of APIs as a target for POSTs from services like Tropo.  You can then retrieve the POST data from the web site, and use CURL on your local machine to POST to the service running locally to see the output of your function.  A command like this would work:

` curl -X POST -H "key: DevTropo" localhost:15005/ -d @tropo_request_sample.json`

The downside to this is that the response and action don't make it back to Tropo where it can send messages back to users.

More detailed suggestions on developing services like this are beyond the scope of this README.

Each of the services in the application (i.e. myhero_web, myhero_app, and myhero_data) include Vagrant support to allow working locally on all three simultaneously.

**In development, not ready for use yet**

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

# Local Development with Vagrant
**EDIT NEEDED, VAGRANT NOT SETUP YET**

I've included the configuration files needed to do local development with Vagrant in the repo.  Vagrant will still use Docker for local development and is configured to spin up a CentOS7 host VM for running the container.

Before running `vagrant up` you will need to finish the Vagrant file configuration by adding the Spark Account Email and Token to the environment variables used by the container.  To do this:

* Make a copy of Vagrantfile.sample to use
  * `cp Vagrantfile.sample Vagrantfile`
* Edit `Vagrantfile` and add your details where indicated
  * `vim Vagrantfile`
  * Change the value for `myherospark_bot_email` and `spark_token` in the `docker.env` hash

To start local development run:
* `vagrant up`
  - You may need to run this twice.  The first time to start the docker host, and the second to start the container.
* Now you can interact with the API or interface at localhost:15001 (configured in Vagrantfile and Vagrantfile.host)
  - example:  from your local machine `curl -H "key: DevBot" http://localhost:15003/demoroom/members`
  - Environment Variables are configured in Vagrantfile for development

Each of the services in the application (i.e. myhero_web, myhero_app, and myhero_data) include Vagrant support to allow working locally on all three simultaneously.

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
* Spark Bot - [hpreston/myhero_spark](https://github.com/hpreston/myhero_spark)
* Tropo WebAPI - [hpreston/myhero_tropo](https://github.com/hpreston/myhero_tropo)

The docker containers are available at
* Data - [hpreston/myhero_data](https://hub.docker.com/r/hpreston/myhero_data)
* App - [hpreston/myhero_app](https://hub.docker.com/r/hpreston/myhero_app)
* Web - [hpreston/myhero_web](https://hub.docker.com/r/hpreston/myhero_web)
* Spark Bot - [hpreston/myhero_spark](https://hub.docker.com/r/hpreston/myhero_spark)
* Tropo WebAPI - [hpreston/myhero_tropo](https://hub.docker.com/r/hpreston/myhero_tropo)

# Tropo Account Requirement
**EDIT NEEDED**

In order to use this service, you will need a Cisco Tropo Account to use.

Creating an account is free and only requires a working email account.  Visit [http://www.tropo.com](http://www.tropo.com) to signup for an account.

## Basic Application Details
**EDIT NEEDED**


Required

* flask
* ArgumentParser
* requests

# Environment Installation

    pip install -r requirements.txt

# Basic Usage

In order to run, the service needs several pieces of information to be provided:
* App Server Address
* App Server Authentication Key to Use

These details can be provided in one of three ways.
* As a command line argument
  - `python myhero_tropo/myhero_tropo.py --app "http://myhero-app.server.com" --appkey "APP AUTH KEY"`
* As environment variables
  - `export myhero_app_server=http://myhero-app.server.com`
  - `export myhero_app_key=APP AUTH KEY`
  - `python myhero_tropo/myhero_tropo.py`

* As raw input when the application is run
  - `python myhero_tropo/myhero_tropo.py`
  - `What is the app server address? http://myhero-app.server.com`
  - `App Server Key: APP AUTH KEY`

A command line argument overrides an environment variable, and raw input is only used if neither of the other two options provide needed details.

# Accessing
**EDIT NEEDED**


## Interacting with the Tropo Interface
**EDIT NEEDED**

The Tropo Interface is a very simple interface that is designed to make it intuitive to use.  Once in the room, simply say "hello", "help" (or anything else) to have the bot reply back with some instructions on how to access the features.

The servie is deisgned to look for key words to act on, and provide the basic help message for anything else.  The key words are:

* options
  * return a list of the current available options to vote on
* results
  * list the current status of voting results
* vote
  * send a private message to the sender to start a voting session
  * in the private room typing the name of one of the options will register a vote and end the session

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

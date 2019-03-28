# Server-Client Messenger
[![Build Status](https://travis-ci.org/jakubski/MessengerServer.svg?branch=master)](https://travis-ci.org/jakubski/MessengerServer) [![Documentation Status](https://readthedocs.org/projects/messenger-server/badge/?version=latest)](https://messenger-server.readthedocs.io/en/latest/?badge=latest)

## Server
This is an attempt at a simple **server** that manages text communication between **client** applications. So far it is entirely based on Python's standard library (i.e. *socket* and *sqlite3* interfaces).

Current functionalities include:
 - registration
 - logging in
 - adding users to the contact list
 - updating users of their contacts' status change
 - exchanging messages between logged-in users

#### Setup and usage
Python 3.6 is required to run the application. 
The package is equipped with a *setup* script which enables respective modules to "see" each other:
```sh
$ python setup.py install
```
Running the *server* module starts the server:
```sh
$ python server.py
```
#### Documentation
Server documentation is hosted at [readthedocs.io](https://messenger-server.readthedocs.io).
The protocol that both sides of communication are meant to follow can be found on the [Wiki](https://github.com/jakubski/MessengerServer/wiki/Protocol) page.

## Client
A .NET implementation of a client-side application in development at [/adamkuder/MessengerClient](https://github.com/adamkuder/MessengerClient).

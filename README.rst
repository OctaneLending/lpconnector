lpconnector
===========

Python client for syncing LastPass Enterprise with a remote directory over LDAP

Purpose
-------

This client connects to a remote user directory and queries users and groups over LDAP to sync an organization's users and groups in LastPass Enterprise.  The included LastPass API client contains full coverage of the LastPass Enterprise API as documented `here
<https://lastpass.com/enterprise_apidoc.php>`_. This client is designed to be run manually to provision new users and force updates to existing users and to be run in an automated fashion to keep LastPass Enterprise users up-to-date.

Setup
-----

Before installing the client run::

    $ mv .env.template .env

And then update the ``.env`` file with the proper paramters to connect to your user directory and LastPass Enterprise account. Refer to the LastPass Enterprise API documentation linked above to find your account's CID and API key

Usage
-----

Client commands are as follows::

    lpconnector sync
    lpconnector provision [--users=UIDS] [--password=PWD] [--reset-password=BOOL]
    lpconnector getldapusers [--users=UIDS]
    lpconnector getlastpassusers [--email=EMAIL] [--disabled=BOOL] [--admin=BOOL]
    lpconnector (-h | --help)

Options
-------

Details on command options are as follows::

    -h --help               Show help
    --users=UIDS            Comma separated list of uids to provision
    --password=PWD          Default password for provisioned users
    --reset-password=BOOL   Reset the default password [default: True]
    --email=EMAIL           Get a single user by their full email address
    --disabled=BOOL         Get only disabled users
    --admin=BOOL            Get only admin users

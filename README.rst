lpconnector
===========

Python client for syncing LastPass Enterprise with a remote directory over LDAP

Purpose
-------

LastPass currently only offers and AD connector client that works with a local AD server.  This client is intended to connect to a remote user directory and queries users and groups over LDAP to sync an organization's users and groups in LastPass Enterprise.  The included LastPass API client contains *almost* full coverage of the LastPass Enterprise API as documented `here
<https://lastpass.com/enterprise_apidoc.php>`_. This client is designed to be run manually to provision new users and force updates to existing users through the ``provision`` command and to be run in an automated fashion using the ``sync`` command to keep LastPass Enterprise users up-to-date.

PLEASE NOTE: The client is not fully unittested or documented, all of that will be coming soon :)

Prerequisites
-------------

This client requires ``pip`` and ``virtualenv`` with ``setuptools`` to build and run.  The client should work on all operating systems and is compatible with all versions of Python except or 3.7 due to the use of the ``ConfigParser`` module.  This incompatibility will be addressed in a future release.

Setup
-----

Clone this repo to your workspace.  Before installing the client run::

    $ mv src/lpconnector/config/config.ini.template src/lpconnector/config/config.ini

And then update the ``config.ini`` file with the proper parameters to connect to your user directory and LastPass Enterprise account. Refer to the LastPass Enterprise API documentation linked above to find your account's CID and API key.
Then setup and activate your virtual environment and install by running::

    $ virtualenv venv
    $ source venv/bin/activate
    $ python setup.py install

The client can be run like so::

    $ lpconnector <command> [options]

Running Tests
-------------

Setup your virtual environment the same way as above and run::

    $ python setup.py test

Tests use the ``pytest`` module and provide code coverage information via the ``pytest-cov`` module

Usage
-----

Client commands are as follows:

============== ============================================================== =====================================================================
Command Name   Purpose                                                        Options
============== ============================================================== =====================================================================
sync           Sync directory data with LastPass users, intended to scheduled --users or --groups, --no-add, --no-delete, --no-update, --dry-run
provision      Add new users from your directory to LastPass                  --users or --groups, --throttle --password --reset-password --dry-run
ldapusers      Return all users in your directory                             --users or --groups
ldapgroups     Return all groups in your directory                            --groups
lastpassusers  Return all users in LastPass                                   --email, --url, --disabled, --admin, --dry-run
lastpassgroups Return all groups in LastPass                                  --url, --dry-run
getconfig      Return the current config values                               None
help           Print help screen                                              None
============== ============================================================== =====================================================================

Options
-------

Details on command options are as follows:

===================== =========================================================================================== ============================================================================================
Option                Usage                                                                                       Values                                                                                       
===================== =========================================================================================== ============================================================================================
--users=UIDs          Only select specific directory users                                                        Comma separated list of directory users' uids
--groups=GCNs         Only select specific directory groups                                                       Comma separated list of directory groups' common names. Double quote group names with spaces
--no-add              Don't add new users on sync                                                                 None
--no-delete           Don't delete old users on sync                                                              None
--no-update           Don't update user groups on sync                                                            None
--throttle=NUM        Throttle provisioning to batches of NUM users                                               Integer
--password=PWD        Set the default password on new LastPass accounts                                           String. Double quote if password contains spaces
--no-reset-password   Don't reset the default password on first login (requires --password)                       None
--email=EMAIL         Only return a specific LastPass user                                                        Valid email address
--url=URL             Define a different endpoint for the LastPass API                                            Valid url
--disabled=BOOL       Return only disabled or no disabled LastPass users (omitting returns both)                  Boolean or 0/1
--admin=BOOL          Return only admins or only non-admin LastPass Users (omitting returns both)                 Boolean or 0/1
--dry-run             Print payloads to the LastPass API instead of posting them (still retrieves data live data) None
===================== =========================================================================================== ============================================================================================
    
Authors
-------

* Joshua Marcus-Hixson (jixson12_) - *Initial Work*

.. _jixson12: https://www.github.com/jixson12

License
-------

Copyright 2018, Octane Lending, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

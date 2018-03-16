# lastpass-ldap-sync
Python client for syncing LastPass Enterprise with our directory over LDAP

Before using this client you need to create a .env file that contains the neccesarry credentials for your LDAP server and you LastPass Enterprise account. Refer ldap_server.py and lastpass_client.py for the environment variable names expected

Don't forget to setup a virtual environment and run `pip install -r requirements` before using the client
```
Usage:
    connector.py sync
    connector.py provision [--users=UIDS] [--password=PWD] [--reset-password=BOOL]
    connector.py getldapusers [--users=UIDS]
    connector.py getlastpassusers [--email=EMAIL] [--disabled=BOOL] [--admin=BOOL]
    connector.py (-h | --help)

Options:
    -h --help               Show help
    --users=UIDS            Comma separated list of uids to provision
    --password=PWD          Default password for provisioned users
    --reset-password=BOOL   Reset the default password [default: True]
    --email=EMAIL           Get a single user by their full email address
    --disabled=BOOL         Get only disabled users
    --admin=BOOL            Get only admin users
```

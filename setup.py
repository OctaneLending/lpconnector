import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "lpconnector"
    verison = "0.1"
    url = "https://github.com/OctaneLending/lastpass-ldap-syc"
    author = "Joshua Marcus-Hixson"
    author_email = "josh@octanelending.com"
    description = "Connect remote LDAP to LastPass Enterprise API"
    packages=['lpconnector']
    long_description=read('README.rst')

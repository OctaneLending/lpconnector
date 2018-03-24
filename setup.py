import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="lpconnector",
    version="0.2.0",
    url="https://www.github.com/OctaneLending/lastpass-ldap-syc",
    author="Joshua Marcus-Hixson",
    author_email="josh@octanelending.com",
    description="Connect remote LDAP to LastPass Enterprise API",
    platforms="any",
    install_requires=[
        'python-ldap==3.0.0',
        'requests==2.18.4',
        'docopt==0.6.2',
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    package_data={'lpconnector': ['config/*.ini']},
    long_description=read('README.rst'),
    entry_points={
        'console_scripts': [
            'lpconnector=lpconnector.__main__:main',
        ],
    },
)

import io
import sys
from glob import glob
from os.path import basename, dirname, join, splitext
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read(fname):
    return io.open(join(dirname(__file__), fname)).read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            'config',
            '--config=../lpconnector/config/config.ini',
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="lpconnector",
    version='0.4.0',
    url="https://www.github.com/OctaneLending/lastpass-ldap-syc",
    author="Joshua Marcus-Hixson",
    author_email="josh@octanelending.com",
    description="Connect remote LDAP to LastPass Enterprise API",
    platforms="any",
    tests_require=['pytest', 'pytest-cov'],
    install_requires=[
        'python-ldap==3.0.0',
        'requests==2.18.4',
        'docopt==0.6.2',
        'pylint==1.8.3',

    ],
    cmdclass={'test': PyTest},
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.rst'),
    test_suite='tests.test_lpconnector',
    entry_points={
        'console_scripts': [
            'lpconnector=lpconnector.__main__:main',
        ],
    },
    extras_require={
        'testing': ['pytest', 'pytest-cov']
    },
)

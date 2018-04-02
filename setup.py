import io
from glob import glob
from os.path import basename, dirname, join, splitext
from setuptools import setup, find_packages


def read(fname):
    return io.open(join(dirname(__file__), fname)).read()


setup(
    name="lpconnector",
    version='0.4.0',
    url="https://www.github.com/OctaneLending/lastpass-ldap-syc",
    author="Joshua Marcus-Hixson",
    author_email="josh@octanelending.com",
    description="Connect remote LDAP to LastPass Enterprise API",
    platforms="any",
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-sugar', 'docopt'],
    install_requires=[
        'python-ldap==3.0.0',
        'requests==2.18.4',
        'docopt==0.6.2',
        'pylint==1.8.3',

    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.rst'),
    entry_points={
        'console_scripts': [
            'lpconnector=lpconnector.__main__:main',
        ],
    },
)

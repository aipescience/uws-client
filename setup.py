# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
from subprocess import check_output, CalledProcessError

install_requires = [
    "argparse>=1.2.1",
    "texttable>=0.8.1",
    "lxml"
]

# get the long_description from the README
with open('README.md') as f:
    long_description = f.read()

# get the current tag using git describe
try:
    tag = check_output(["git", "describe", "--tags"]).strip()
except CalledProcessError:
    sys.exit('Error: current HEAD is not tagged.')

setup(
    name='uws-client',
    version=tag,
    url='http://github.com/aipescience/uws-client/',
    download_url='http://github.com/aipescience/uws-client/archive/%s.tar.gz' % tag,
    packages=find_packages(),
    license=u'Apache License (2.0)',
    author=u'AIP E-Science - Adrian M. Partl',
    maintainer=u'Adrian M. Partl',
    maintainer_email=u'adrian@partl.net',
    description=u'a command line client for IVOA UWS services, plus models for development',
    long_description=long_description,
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['uws = uws.cli.main:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ]
)

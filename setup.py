# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from subprocess import check_output, CalledProcessError

install_requires = [
    "argparse>=1.2.1",
    "texttable>=0.8.1",
    "lxml",
    "python-dateutil",
    "pytz"
]

version = "1.1.11"

setup(
    name='uws-client',
    version=version,
    url='http://github.com/aipescience/uws-client/',
    download_url='http://github.com/aipescience/uws-client/archive/%s.tar.gz' % version,
    packages=find_packages(),
    license=u'Apache License (2.0)',
    author=u'Adrian M. Partl',
    author_email='adrian@partl.net',
    maintainer=u'AIP E-Science',
    maintainer_email=u'escience@aip.de',
    description=u'A command line client for IVOA UWS services, plus models for development',
    long_description='This is a client for IVOA Virtual Observatroy UWS services. It can be used to access UWS services directly or through Basic Authentication. Please visit https://github.com/aipescience/uws-client/blob/master/README.md for how to use the software.',
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

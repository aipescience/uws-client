# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    description = f.read()

install_requires = [
    "argparse>=1.2.1",
    "texttable>=0.8.1",
    "lxml"
]

setup(
    name='uws',
    url='http://github.com/aipescience/uws-client/',
    version='0.1.0',
    packages=find_packages(),
    license=u'Apache License (2.0)',
    author=u'AIP eScience - Adrian M. Partl',
    maintainer=u'Adrian M. Partl',
    maintainer_email=u'adrian@partl.net',
    description=u'a command line client for IVOA UWS services, plus models for development',
    long_description=description,
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
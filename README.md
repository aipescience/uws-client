uws - A client for UWS IVOA services
====================================

[![Build Status](https://travis-ci.org/aipescience/uws-client.svg?branch=travis_ci)](https://travis-ci.org/aipescience/uws-client)

This is a client for IVOA Virtual Observatroy UWS services.
It can be used to access UWS services directly or through Basic
Authentication.

Installation:
-------------

In a directory of your choice, clone uws-client from the AIP 
E-Science repository:

```
git clone https://github.com/aipescience/uws-client
```

You might need to install the headers of the xml libraries for your system. e.g for debian/Ubuntu:

```
apt-get install libxml2-dev libxslt1-dev python-dev
```

Then install the python package using pip:

```
cd uws-client
pip install .
```

This will install `uws` into your systems `bin` directory and
makes the command available on the command line.

Running unit tests:
-------------------

If you want to make sure that uws client works as we have anticipated
it, you are free to run the unittests. For this you need to setup the
development environment in the `uws-client` directory:

```
pip install -r ./requirements.pip
pip install -r ./requirements-dev.pip
```

You can then run the unittests using nosetests:

```
cd uws
nosetests .
```

Generic usage of the uws client:
--------------------------------

usage: `uws [-h] -H HOST [-U USER] [-P] {job,list} ...`

positional arguments:  
    `{job,list}`         commands for UWS  
    `list`               list all jobs on the UWS service  
    `job`                access a given job on the UWS service  

optional arguments:  
  `-h`, `--help`            show this help message and exit  
  `-H HOST`, `--host HOST`  URL to UWS service  
  `-U USER`, `--user USER`  user name  
  `-P` , `--password PWD`   password (`-P`: use prompt)  


List all jobs on service:
-------------------------

usage: `uws list [-h] [-c] [-p] [-q] [-e] [-E] [-a] [--unknown] [--held]
                   [--suspended] [--archived]`

optional arguments:  
  `-h`, `--help`       show this help message and exit  
  `-c`, `--completed`  show completed jobs  
  `-p`, `--pending`    show pending jobs  
  `-q`, `--queued`     show queued jobs  
  `-e`, `--executing`  show executing jobs  
  `-E`, `--error`      show jobs with errors  
  `-a`, `--aborted`    show aborted jobs  
  `--unknown`          show unknown state jobs  
  `--held`             show held jobs  
  `--suspended`        show suspended jobs  
  `--archived`         [UWS1.1] show (deleted) jobs archived on the server  
  `--after TIMESTAMP`  [UWS1.1] show only jobs started after given UTC time,
                        also works with local time, if timezone information is added (e.g. --after 2015-09-10T10:00+02:00 for European/Paris, day saving time)  
  `--last  NUMBER`     [UWS1.1] show only NUMBER most recently started jobs

Specifying any of the specific job phases will only show those jobs with the
corresponding phase. You can even combine two or more phases by appending multiple phase filters, e.g. if you want all jobs with phase ERROR and additionally the ABORTED jobs, then use `--error --aborted`.


Job handling:
-------------

usage: `uws job [-h] {set,run,show,phase,results,abort,new,delete} ...`  

positional arguments:  
  {`set`,`run`,`show`,`phase`,`results`,`abort`,`new`,`delete`}
                          commands for manipulating jobs  
    `show`                show the specific job  
    `new`                 create a new job  
    `set`                 set parameters for the specific job  
    `run`                 run the specific job if its state is pending  
    `phase`               show the phase of a specific job  
    `abort`               aborts the execution of a specific job  
    `delete`              delete a specific job  
    `results`             download results of a specific job  

optional arguments:  
  `-h`, `--help`            show this help message and exit  


Show job:
---------

usage: `uws job show [-h] id [-w [WAIT]] [-s PHASE] `

positional arguments:  
  `id`          `job id`

optional arguments:  
  `-h`, `--help`                show this help message and exit  
  `-w [WAIT]`, `--wait [WAIT]`  [UWS1.1] wait for phase change before returning, but at most the specified amount of seconds or infinitely, if no value is given  
  `-s PHASE`, `--phase PHASE`   [UWS1.1] required phase while waiting  


New job:
--------

usage: `uws job new [-h] [-r] [job_parameters [job_parameters ...]]`

positional arguments:  
  `job_parameters`   unspecified list of UWS service parameters in the form
                   `<parameter>=<value>`.  
                   Default parameters are:  
                   `destruction` (Destruction time of the job),  
                   `executionDuration` (Execution duration of the job in seconds)  

optional arguments:  
  `-h`, `--help`  show this help message and exit  
  `-r`, `--run`   immediately submits the job on creation  

Job parameters are given at the end of the command in the following format:  
  `<parameter>=<value>`  
eg: `executionDuration=20`, `query="SELECT * FROM foo"`  

Be aware, that a UWS service can have additional parameters for a job than the
standardised `destruction` and `executionDuration` parameter.

There is no way to know which parameters are supported by a UWS service, so the
service provider needs to be contacted or its documentation consulted.


Set parameters for existing job:
--------------------------------

usage: `uws job set [-h] id [job_parameters [job_parameters ...]]`  

positional arguments:  
  `id`          job id  
  `job_parameters`   unspecified list of UWS service parameters in the form
                     `<parameter>=<value>`.  
                     Default parameters are:  
                     `destruction` (Destruction time of the job),  
                     `executionDuration` (Execution duration of the job in seconds)  

optional arguments:  
  `-h`, `--help`  show this help message and exit  


Job parameters are specified as with creating new jobs.


Run / submit an existing job:
-----------------------------

usage: `uws job run [-h] id`  

positional arguments:  
  `id`          `job id`

optional arguments:  
  `-h`, `--help`  show this help message and exit


Show phase of job:
------------------

usage: `uws job phase [-h] id`

positional arguments:  
  `id`          `job id`

optional arguments:  
  `-h`, `--help`  show this help message and exit


Download results from a finished job:
-------------------------------------

usage: `uws job results [-h] id [result_id] [-f file_base]`

positional arguments:  
  `id`          job id  
  `result_id`    result id, e.g. for specifying the format  

optional arguments:  
  `-h`, `--help`           show this help message and exit  
  `-f`, `--file_base`      basename of output file, will be appended with result_id  

Results are downloaded to the directory from which uws was called!
(Unless a file_base is given and contains a path.)


Abort or delete an existing job:
--------------------------------

usage: `uws job abort [-h] id`

positional arguments:  
  `id`          job id

optional arguments:  
  `-h`, `--help`  show this help message and exit


usage: `uws job delete [-h] id`

positional arguments:  
  `id`          job id

optional arguments:  
  `-h`, `--help`  show this help message and exit

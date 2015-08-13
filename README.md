uws - A client for UWS IVOA services
====================================

This is a client for IVOA Virtual Observatroy UWS services.
It can be used to access UWS services directly or through Basic
Authentication.

Installation:
-------------

In a directory of your choice, clone uws-client from the AIP 
eScience repository:

`git clone https://github.com/aipescience/uws-client`

Then install the python package using pip:

`cd uws-client`
`pip install .

This will install `uws` into your systems `bin` directory and
makes the command available on the command line.

Below you find a list of supported commands and their usage:

Generic usage:
--------------

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
                   [--suspended]`

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


Specifying any of the specific job phases will only show those jobs with the
corresponding phase


Job handling:
-------------

usage: `uws job [-h] {set,run,show,results,abort,new,delete} ...`

positional arguments:  
  {`set`,`run`,`show`,`results`,`abort`,`new`,`delete`}
                          commands for manipulating jobs
    `show`                show the specific job  
    `new`                 create a new job  
    `set`                 set parameters for the specific job  
    `run`                 run the specific job if its state is pending  
    `abort`               aborts the execution of a specific job  
    `delete`              delete a specific job  
    `results`             download results of a specific job  

optional arguments:  
  `-h`, `--help`            show this help message and exit  


Show job:
---------

usage: `uws job show [-h] id`

positional arguments:  
  `id`          `job id`

optional arguments:  
  `-h`, `--help`  show this help message and exit


New job:
--------

usage: `uws job new [-h] [-r] [jobParams [jobParams ...]]`

positional arguments:  
  jobParams   unspecified list of UWS service parameters in the form
              `<parameter>=<value>` - Default parameters are: `destruction`
              (Destruction time of the job), `executionDuration` (Execution
              duration of the job in seconds)

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

usage: `uws job set [-h] id [jobParams [jobParams ...]]`

positional arguments:  
  `id`          job id  
  `jobParams`   unspecified list of UWS service parameters in the form
              `<parameter>=<value>` - Default parameters are: `destruction`
              (Destruction time of the job), `executionDuration` (Execution
              duration of the job in seconds)

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


Download results from a finished job:
-------------------------------------

usage: `uws job results [-h] id [resultid] [-f filebasename]`

positional arguments:  
  `id`          job id  
  `resultid`    result id, e.g. for specifying the format  

optional arguments:  
  `-h`, `--help`           show this help message and exit  
  `-f`, `--filebasename`   basename of output file, will be appended with resultid  

Results are downloaded to the directory from which uws was called!
(Unless a filebasename is given and contains a path.)


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

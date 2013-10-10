import sys, os

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '../lib'))

from UWS import connection as UWSconnection
from UWS import base as UWSbase

def main():
    UWSconn = UWSconnection.connection("http://escience.aip.de/daiquiri/uws/query", "admin", "xxxxxxxx")
    UWS = UWSbase.base(UWSconn)

    jobs = UWS.getJobList()
    print jobs

    print "Obtaining information on job %s" % jobs.jobref[0].reference.href.rsplit("/", 1)[1]
    job = UWS.getJob(jobs.jobref[0].reference.href.rsplit("/", 1)[1])
    print job


if __name__ == '__main__':
    main()

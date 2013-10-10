import connection as UWSconn
import models as UWSmodels
import sys


class base:
    def __init__(self, connection):
        self.conn = connection

    def getJobList(self):
        res = self.conn.get('')
        raw = res.read()
        jobList = UWSmodels.jobs(raw)
        return jobList

    def getJob(self, id):
        res = self.conn.get(id)
        raw = res.read()
        return UWSmodels.job(raw)

    def newJob(self, args={}):
        res = self.conn.post('', args)
        raw = res.read()
        print raw
        return UWSmodels.job(raw)

    def setParamsJob(self, id, args={}):
        res = self.conn.post(id, args)
        raw = res.read()
        return UWSmodels.job(raw)

    def runJob(self, id):
        res = self.conn.post(id, {"phase": "run"})
        raw = res.read()
        return UWSmodels.job(raw)

    def abortJob(self, id):
        res = self.conn.post(id, {"phase": "abort"})
        raw = res.read()
        return UWSmodels.job(raw)

    def deleteJob(self, id):
        res = self.conn.delete(id)
        raw = res.read()
        return True

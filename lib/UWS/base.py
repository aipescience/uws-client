import connection as UWSconn
import models as UWSmodels
from lxml.etree import XMLSyntaxError as XMLSyntaxError

import sys


class base:
    def __init__(self, connection):
        self.conn = connection

    def getJobList(self):
        try:
            res = self.conn.get('')
        except RuntimeError, e:
            raise UWSerror(str(e))

        raw = res.read()

        try:
            jobList = UWSmodels.jobs(raw)
        except XMLSyntaxError, e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception, e:
            raise e

        return jobList

    def getJob(self, id):
        try:
            res = self.conn.get(id)
        except RuntimeError, e:
            raise UWSerror(str(e))

        raw = res.read()
        try:
            result = UWSmodels.job(raw)
        except XMLSyntaxError, e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception, e:
            raise e

        return result

    def newJob(self, args={}):
        try:
            res = self.conn.post('', args)
        except RuntimeError, e:
            raise UWSerror(str(e))

        raw = res.read()
        try:
            result = UWSmodels.job(raw)
        except XMLSyntaxError, e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception, e:
            raise

        return result

    def setParamsJob(self, id, args={}):
        try:
            res = self.conn.post(id, args)
        except RuntimeError, e:
            raise UWSerror(str(e))

        raw = res.read()
        try:
            result = UWSmodels.job(raw)
        except XMLSyntaxError, e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception, e:
            raise e

        return result

    def runJob(self, id):
        try:
            res = self.conn.post(id, {"phase": "run"})
        except RuntimeError, e:
            raise UWSerror(str(e))

        raw = res.read()
        try:
            result = UWSmodels.job(raw)
        except XMLSyntaxError, e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception, e:
            raise e

        return result

    def abortJob(self, id):
        try:
            res = self.conn.post(id, {"phase": "abort"})
        except RuntimeError, e:
            raise UWSerror(str(e))

        raw = res.read()
        try:
            result = UWSmodels.job(raw)
        except XMLSyntaxError, e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception, e:
            raise e

        return result

    def deleteJob(self, id):
        try:
            res = self.conn.delete(id)
        except RuntimeError, e:
            raise UWSerror(str(e))

        raw = res.read()
        try:
            result = True
        except XMLSyntaxError, e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception, e:
            raise e

        return result

class UWSerror(Exception):
    def __init__(self, msg, raw = False):
        self.msg = msg
        self.raw = raw

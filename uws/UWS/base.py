# -*- coding: utf-8 -*-
import models as models
from lxml.etree import XMLSyntaxError as XMLSyntaxError


class BaseUWSClient(object):
    def __init__(self, connection):
        self.connection = connection

    def get_job_list(self):
        try:
            response = self.connection.get('')
        except RuntimeError as e:
            raise UWSerror(str(e))

        raw = response.read()

        try:
            job_list = models.Jobs(raw)
        except XMLSyntaxError as e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return job_list

    def get_job(self, id):
        try:
            response = self.connection.get(id)
        except RuntimeError as e:
            raise UWSerror(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return result

    def new_job(self, args={}):
        try:
            response = self.connection.post('', args)
        except RuntimeError as e:
            raise UWSerror(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise

        return result

    def set_params_job(self, id, args={}):
        try:
            response = self.connection.post(id, args)
        except RuntimeError as e:
            raise UWSerror(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return result

    def run_job(self, id):
        try:
            response = self.connection.post(id + '/phase', {"phase": "RUN"})
        except RuntimeError as e:
            raise UWSerror(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return result

    def abort_job(self, id):
        try:
            response = self.connection.post(id, {"phase": "abort"})
        except RuntimeError as e:
            raise UWSerror(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return result

    def delete_job(self, id):
        try:
            response = self.connection.delete(id)
        except RuntimeError as e:
            raise UWSerror(str(e))

        raw = response.read()
        try:
            result = True
        except XMLSyntaxError as e:
            raise UWSerror("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return result


class UWSerror(Exception):
    def __init__(self, msg, raw=False):
        self.msg = msg
        self.raw = raw

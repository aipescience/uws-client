# -*- coding: utf-8 -*-
from lxml.etree import XMLSyntaxError as XMLSyntaxError

import models
from datetime import datetime
import dateutil.parser

class BaseUWSClient(object):
    def __init__(self, connection):
        self.connection = connection

    def get_job_list(self, filters):
        params = None
        if filters:
            params = self._validate_and_parse_filters(filters)
            print 'params: ', params ## debug

        try:
            response = self.connection.get('', params)
        except:
            try:
                response = self.connection.get('')
            except Exception as e:
                raise UWSError(str(e))

        raw = response.read()

        try:
            job_list = models.Jobs(raw)
        except XMLSyntaxError as e:
            raise UWSError("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return job_list

    def _validate_and_parse_filters(self, filters):
        filters_copy = filters.copy()
        phases = filters_copy.pop('phases', None)
        after = filters_copy.pop('after', None)
        last = filters_copy.pop('last', None)

        if filters_copy:
            raise UWSError("Unknown filter properties %s", filters_copy.keys())

        params = []

        if phases:
            for phase in phases:
                if phase not in models.JobPhases.phases:
                    raise UWSError("Unknown phase %s in filter", phase)
                params.append(("PHASE", phase))

        if after:
            # TODO: Allow to provide local time and convert here to UTC?
            # TODO: We may encounter more troubles with microseconds, if ',' used instead of '.'(e.g. German systems)

            try:
                date = dateutil.parser.parse(after)
                # TODO: The day defaults to '05' if no day is given (e.g. '2010-09'->'2010-09-05'), not to '01'. Is this OK?
            except:
                raise UWSError("Date time format could not be parsed, expecting UTC in ISO 8601:2004 format or compatible: %s" % (str(after)))
            date = datetime.isoformat(date)
            params.append(("AFTER", date))

        if last:
            notint = False
            try:
                last = int(last)
            except:
                notint = True
            if notint or last < 0:
                raise UWSError("Value for 'last' argument must be a positive integer: %s" % (str(last)))
            params.append(("LAST", last))

        return params

    def get_job(self, id):
        try:
            response = self.connection.get(id)
        except Exception as e:
            raise UWSError(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSError("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e
            # TODO: had problems with "raise e" here: AttributeError: 'NoneType' object has no attribute 'text'

        return result

    def get_phase(self, id):
        try:
            response = self.connection.get(id + '/phase')
        except Exception as e:
            raise UWSError(str(e))

        raw = response.read()
        result = raw
        
        return result

    def new_job(self, args={}):
        try:
            response = self.connection.post('', args)
        except Exception as e:
            raise UWSError(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSError("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise

        return result

    def set_params_job(self, id, args={}):
        try:
            response = self.connection.post(id, args)
        except Exception as e:
            raise UWSError(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSError("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return result

    def run_job(self, id):
        try:
            response = self.connection.post(id + '/phase', {"PHASE": "RUN"})
        except Exception as e:
            raise UWSError(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSError("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return result

    def abort_job(self, id):
        try:
            response = self.connection.post(id, {"PHASE": "ABORT"})
        except Exception as e:
            raise UWSError(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSError("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return result

    def delete_job(self, id):
        try:
            response = self.connection.delete(id)
        except Exception as e:
            raise UWSError(str(e))

        raw = response.read()
        try:
            result = True
        except XMLSyntaxError as e:
            raise UWSError("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

        return result


class UWSError(Exception):
    def __init__(self, msg, raw=False):
        self.msg = msg
        self.raw = raw

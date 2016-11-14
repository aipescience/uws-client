# -*- coding: utf-8 -*-
from lxml.etree import XMLSyntaxError as XMLSyntaxError

import connection as UWSConnection
import models
from errors import UWSError
from datetime import datetime
import dateutil.parser
import pytz


class Client(object):
    def __init__(self, url=None, user=None, password=None, connection=None):
        if connection:
            self.connection = connection
        else:
            self.connection = UWSConnection.Connection(url, user, password)

    def get_job_list(self, filters=None):
        params = None
        if filters:
            params = self._validate_and_parse_filters(filters)
            # print 'params: ', params ## debug

        try:
            response = self.connection.get('', params)
        except Exception as e:
            # Do not try to make a second request without parameters here,
            # because cannot call self.connection.get() a second time and reusing the connection
            # without calling a getresponse() or close() or something beforehand.
            # (This would lead to a httplib CannotSendRequest() error!)
            # Let's just raise the error immediately.
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
                # The day defaults to current day, not to '01', if no day is
                # given (e.g. '2010-09'->'2010-09-06').
                # Let's tell the user how the given value was interpreted:
                if str(date) != str(after):
                    print "Note: Changed value for keyword 'after' from '%s' to '%s'." % (after, str(date))

            except:
                raise UWSError("Date time format could not be parsed, expecting UTC in ISO 8601:2004 format or compatible: %s" % (str(after)))

            # Convert from given time (with attached timezone information) to UTC time
            if date.utcoffset() is not None:
                utz = pytz.timezone('UTC')
                date = date.astimezone(utz).replace(tzinfo=None)
                print "Note: Date time was converted to UTC time: %s" % (str(date))

            date = date.isoformat()
            params.append(("AFTER", date))

        if last:
            try:
                last = int(last)
            except:
                raise UWSError("Value for 'last' argument must be a positive integer: %s" % (str(last)))

            if last < 1:
                raise UWSError("Value for 'last' argument must be a positive integer: %s" % (str(last)))
            params.append(("LAST", last))

        return params

    def _validate_and_parse_wait(self, wait, phase=None):
        # wait must be positive integer or -1
        if wait.isdigit() or wait == '-1':
            duration = int(wait)
        else:
            raise UWSError("Value for wait-keyword must be positive integer or -1: %s" % str(wait))

        params = [("WAIT", duration)]

        if phase:
            if phase not in models.JobPhases.active_phases:
                raise UWSError("Given phase '%s' is not an active phase, 'wait' with this phase is not supported." % phase)
            params.append(("PHASE", phase))

        return params

    def get_job(self, id, wait=None, phase=None):
        params = None
        if wait:
            params = self._validate_and_parse_wait(wait, phase)

        try:
            response = self.connection.get(id, params)
        except Exception as e:
            # Do not make a second request without params, throw error
            # immediately
            raise UWSError(str(e))

        raw = response.read()
        try:
            result = models.Job(raw)
        except XMLSyntaxError as e:
            raise UWSError("Malformatted response. Are you sure the host you specified is a IVOA UWS service?", raw)
        except Exception as e:
            raise e

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

    def set_parameters_job(self, id, args={}):
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

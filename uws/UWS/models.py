# -*- coding: utf-8 -*-
from lxml import etree as et


class BaseUWSModel(object):
    def _parse_bool(self, value):
        if isinstance(value, str):
            if value.lower() == 'true':
                return True
            return False
        return value

    def _find_uws_namespace(self, namespaces):
        # Search for namespace that contains "http://www.ivoa.net/xml/UWS/"
        # (usually, there is a version attached, which we ignore here),
        # for using it (including {}) as uws_namespace in the
        # find/findall-functions everywhere below.
        namespace = None
        namespace = next(value for key, value in namespaces.iteritems()
                            if 'http://www.ivoa.net/xml/UWS/' in value)
        
        if namespace is None:
            raise RuntimeError("No matching UWS namespace found in xml-response, cannot parse xml.")
        else:
            uws_namespace = '{' + namespace + '}'

        return uws_namespace


class Jobs(BaseUWSModel):
    def __init__(self, xml=None):
        self.job_reference = None

        if xml is not None:
            # parse xml
            parsed = et.fromstring(xml)
            uws_namespace = self._find_uws_namespace(parsed.nsmap)

            xml_jobs = parsed.findall(uws_namespace+'jobref', namespaces=parsed.nsmap)

            self.job_reference = []
            for xmlJob in xml_jobs:
                self.add_job(
                    job=JobRef(xml_node=xmlJob, xml_namespace=parsed.nsmap, uws_namespace=uws_namespace)
                )

        else:
            self.job_reference = []

    def __unicode__(self):
        str = ""
        for job in self.job_reference:
            str += unicode(job) + "\n"
        return str

    def __str__(self):
        return unicode(self).encode('utf-8')

    def add_job(self, id=None, href=None, phase=None, job=None):
        if job is not None:
            self.job_reference.append(job)
        else:
            reference = Reference(href=href, type="simple")
            job_reference = JobRef(id=id, phase=phase, reference=reference)
            self.job_reference.append(job_reference)


class JobRef(BaseUWSModel):
    def __init__(self, id=None, phase=None, reference=None, xml_node=None, xml_namespace=None, uws_namespace=''):
        self.id = None
        self.reference = Reference()
        self.phase = []

        if xml_node is not None:
            self.id = xml_node.get('id')

            # UWS standard defines array, therefore treat phase as array
            self.phase = [elm.text for elm in xml_node.findall(uws_namespace+'phase', namespaces=xml_namespace)]
            self.reference = Reference(xml_node=xml_node, xml_namespace=xml_namespace)
        elif id is not None and phase is not None and reference is not None:
            self.id = id

            if isinstance(phase, basestring):
                self.phase = [phase]
            else:
                self.phase = phase

            if isinstance(reference, Reference):
                self.reference = reference
            else:
                raise RuntimeError("Malformated reference given in jobref id: %s" % id)

    def set_phase(self, new_phase):
        self.phase = [new_phase]

    def __unicode__(self):
        return "Job '%s' in phase '%s' - %s" % (self.id, ', '.join(self.phase), unicode(self.reference))

    def __str__(self):
        return unicode(self).encode('utf-8')


class Reference(BaseUWSModel):
    def __init__(self, href=None, type=None, xml_node=None, xml_namespace=None):
        self.type = "simple"
        self.href = ""

        if xml_node is not None:
            # TODO: properly check for the namespace that contains xlink,
            # namespace prefix may differ from xlink!
            # (e.g. xl:href instead of xlink:href)
            self.type = xml_node.get('{%s}type' % xml_namespace['xlink'])
            self.href = xml_node.get('{%s}href' % xml_namespace['xlink'])
        elif href is not None and type is not None:
            self.type = type
            self.href = href

    def __unicode__(self):
        return self.href

    def __str__(self):
        return unicode(self).encode('utf-8')


class Job(BaseUWSModel):
    def __init__(self, xml=None):
        self.job_id = None
        self.run_id = None
        self.owner_id = None
        self.phase = ["PENDING"]
        self.quote = None
        self.start_time = None
        self.end_time = None
        self.execution_duration = 0
        self.destruction = None
        self.parameters = []
        self.results = []
        self.error_summary = None
        self.job_info = []

        if xml is not None:
            # parse xml
            parsed = et.fromstring(xml)

            # again find proper UWS namespace-string as prefix for search paths in find
            uws_namespace = self._find_uws_namespace(parsed.nsmap)

            self.job_id = parsed.find(uws_namespace + 'jobId', namespaces=parsed.nsmap).text

            self.run_id = self._get_optional(parsed, uws_namespace + 'runId')

            self.owner_id = parsed.find(uws_namespace + 'ownerId', namespaces=parsed.nsmap).text
            self.phase = [parsed.find(uws_namespace + 'phase', namespaces=parsed.nsmap).text]
            self.quote = self._get_optional(parsed, uws_namespace + 'quote')
            self.start_time = parsed.find(uws_namespace + 'startTime', namespaces=parsed.nsmap).text
            self.end_time = parsed.find(uws_namespace + 'endTime', namespaces=parsed.nsmap).text
            self.execution_duration = int(parsed.find(uws_namespace + 'executionDuration', namespaces=parsed.nsmap).text)
            self.destruction = parsed.find(uws_namespace + 'destruction', namespaces=parsed.nsmap).text

            self.parameters = []
            tmp = parsed.find(uws_namespace + 'parameters', namespaces=parsed.nsmap)
            if tmp is not None:
                parameters = list(tmp)
            for param in parameters:
                self.add_parameter(parameter=Parameter(xml_node=param))

            self.results = []
            tmp = parsed.find(uws_namespace + 'results', namespaces=parsed.nsmap)
            if tmp is not None:
                results = list(tmp)
            for res in results:
                self.add_result(result=Result(xml_node=res, xml_namespace=parsed.nsmap))

            self.error_summary = False
            tmp = parsed.find(uws_namespace + 'errorSummary', namespaces=parsed.nsmap)
            if tmp is not None:
                self.error_summary = ErrorSummary(xml_node=tmp, xml_namespace=parsed.nsmap, uws_namespace=uws_namespace)

            self.job_info = []
            tmp = parsed.find(uws_namespace + 'jobInfo', namespaces=parsed.nsmap)
            if tmp is not None:
                self.job_info = list(tmp)

    def __unicode__(self):
        str = "JobId : '%s'\n" % self.job_id
        str += "RunId : '%s'\n" % self.run_id
        str += "OwnerId : '%s'\n" % self.owner_id
        str += "Phase : '%s'\n" % ', '.join(self.phase)
        str += "Quote : '%s'\n" % self.quote
        str += "StartTime : '%s'\n" % self.start_time
        str += "EndTime : '%s'\n" % self.end_time
        str += "ExecutionDuration : '%s'\n" % self.execution_duration
        str += "Destruction : '%s'\n" % self.destruction

        str += "Parameters :\n"
        for param in self.parameters:
            str += "%s\n" % unicode(param)

        str += "Results :\n"
        for res in self.results:
            str += "%s\n" % unicode(res)

        str += "errorSummary :\n %s\n" % unicode(self.error_summary)

        str += "jobInfo :\n"
        for info in self.job_info:
            str += "%s\n" % unicode(info)

        return str

    def __str__(self):
        return unicode(self).encode('utf-8')

    def add_parameter(self, id=None, by_reference=False, is_post=False, value=None, parameter=None):
        if not parameter:
            parameter = Parameter(id=id, by_reference=by_reference, is_post=is_post, value=value)

        self.parameters.append(parameter)

    def add_result(self, id=None, href=None, result=None):
        if not result:
            reference = Reference(href=href, type="simple")
            result = Result(id=id, reference=reference)

        self.results.append(result)

    def _get_optional(self, parsed, element_name):
        """returns the text value of element_name within the parsed elementTree.

        If element_name doesn't exist, return None.
        """
        option = parsed.find(element_name, namespaces=parsed.nsmap)
        if option is None:
            return None
        else:
            return option.text


class Parameter(BaseUWSModel):
    def __init__(self, id=None, by_reference=False, is_post=False, value=None, xml_node=None):
        self.id = None
        self.by_reference = False
        self.is_post = False
        self.value = None

        if xml_node is not None:
            self.id = xml_node.get('id')
            self.by_reference = self._parse_bool(xml_node.get('by_reference', default=False))
            self.is_post = self._parse_bool(xml_node.get('is_post', default=False))
            self.value = xml_node.text
        elif id is not None and value is not None:
            self.id = id
            self.by_reference = by_reference
            self.is_post = is_post
            self.value = value

    def __unicode__(self):
        return "Parameter id '%s' byRef: %s is_post: %s - value: %s" % (self.id, self.by_reference, self.is_post, self.value)

    def __str__(self):
        return unicode(self).encode('utf-8')


class Result(BaseUWSModel):
    def __init__(self, id=None, reference=None, xml_node=None, xml_namespace=None):
        self.id = None
        self.reference = Reference()

        if xml_node is not None:
            self.id = xml_node.get('id')
            self.reference = Reference(xml_node=xml_node, xml_namespace=xml_namespace)
        elif id is not None and reference is not None:
            self.id = id

            if isinstance(reference, Reference):
                self.reference = reference
            else:
                raise RuntimeError("Malformated reference given in result id: %s" % id)

    def __unicode__(self):
        return "Result id '%s' reference: %s" % (self.id, unicode(self.reference))

    def __str__(self):
        return unicode(self).encode('utf-8')


class ErrorSummary(BaseUWSModel):
    def __init__(self, type="transient", has_detail=False, messages=None,
                 xml_node=None, xml_namespace=None, uws_namespace=''):
        self.type = "transient"
        self.has_detail = False
        self.messages = []

        if xml_node is not None:
            self.type = xml_node.get('type')
            self.has_detail = self._parse_bool(xml_node.get('hasDetail', default=False))

            self.messages = []
            messages = xml_node.findall(uws_namespace + 'message', namespaces=xml_namespace)

            for message in messages:
                self.messages.append(message.text)

        elif messages is not None:
            self.type = type
            self.has_detail = has_detail
            self.messages = messages

    def __unicode__(self):
        return "Error Summary - type '%s' hasDetail: %s - message: %s" % (self.type, self.has_detail, "\n".join(self.messages))

    def __str__(self):
        return unicode(self).encode('utf-8')

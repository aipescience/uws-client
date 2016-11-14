# -*- coding: utf-8 -*-
from lxml import etree as et

uws_1_namespace = "http://www.ivoa.net/xml/UWS/v1.0"
#uws_2_namespace = "http://www.ivoa.net/xml/UWS/v2.0"
xlink_namespace = "http://www.w3.org/1999/xlink"


class UWS1Flavour(object):
    def __init__(self, namespaces=None):

        if uws_1_namespace not in namespaces.values():
            raise RuntimeError("No supported UWS namespace found in xml-response, cannot parse xml.")

        # prepend each element's name with the correct uws-namespace
        # for this version
        self.uws_namespace = uws_1_namespace
        self.jobs = et.QName(self.uws_namespace, "jobs")
        self.jobref = et.QName(self.uws_namespace, "jobref")
        self.phase = et.QName(self.uws_namespace, "phase")
        self.jobId = et.QName(self.uws_namespace, "jobId")
        self.runId = et.QName(self.uws_namespace, "runId")
        self.ownerId = et.QName(self.uws_namespace, "ownerId")
        self.quote = et.QName(self.uws_namespace, "quote")
        self.creationTime = et.QName(self.uws_namespace, "creationTime")
        self.startTime = et.QName(self.uws_namespace, "startTime")
        self.endTime = et.QName(self.uws_namespace, "endTime")
        self.executionDuration = et.QName(self.uws_namespace, "executionDuration")
        self.destruction = et.QName(self.uws_namespace, "destruction")
        self.parameters = et.QName(self.uws_namespace, "parameters")
        self.results = et.QName(self.uws_namespace, "results")
        self.errorSummary = et.QName(self.uws_namespace, "errorSummary")
        self.message = et.QName(self.uws_namespace, "message")
        self.jobInfo = et.QName(self.uws_namespace, "jobInfo")


class JobPhases(object):
    COMPLETED = 'COMPLETED'
    PENDING = 'PENDING'
    QUEUED = 'QUEUED'
    EXECUTING = 'EXECUTING'
    ERROR = 'ERROR'
    ABORTED = 'ABORTED'
    UNKNOWN = 'UNKNOWN'
    HELD = 'HELD'
    SUSPENDED = 'SUSPENDED'
    ARCHIVED = 'ARCHIVED'

    phases = [COMPLETED, PENDING, QUEUED, EXECUTING,
              ERROR, ABORTED, UNKNOWN, HELD,
              SUSPENDED, ARCHIVED]

    # phases for which blocking behaviour can occur:
    active_phases = [PENDING, QUEUED, EXECUTING]

    versions = {
        COMPLETED: ['1.0', '1.1'],
        PENDING: ['1.0', '1.1'],
        QUEUED: ['1.0', '1.1'],
        EXECUTING: ['1.0', '1.1'],
        ERROR: ['1.0', '1.1'],
        ABORTED: ['1.0', '1.1'],
        UNKNOWN: ['1.0', '1.1'],
        HELD: ['1.0', '1.1'],
        SUSPENDED: ['1.0', '1.1'],
        ARCHIVED: ['1.1']
    }


class BaseUWSModel(object):
    def __init__(self):
        self.version = "1.0"

    def _parse_bool(self, value):
        if isinstance(value, str):
            if value.lower() == 'true':
                return True
            return False
        return value


class Jobs(BaseUWSModel):
    def __init__(self, xml=None):
        super(Jobs, self).__init__()

        self.job_reference = None

        if xml is not None:
            # parse xml
            parsed = et.fromstring(xml)

            uws_flavour = UWS1Flavour(parsed.nsmap)

            if parsed.get("version"):
                self.version = parsed.get("version")

            xml_jobs = parsed.findall(uws_flavour.jobref)

            self.job_reference = []

            for xmlJob in xml_jobs:
                self.add_job(
                    job=JobRef(xml_node=xmlJob, xml_namespace=parsed.nsmap, uws_flavour=uws_flavour)
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
    def __init__(self, id=None, phase=None, reference=None, xml_node=None, xml_namespace=None, uws_flavour=None):
        super(JobRef, self).__init__()

        self.id = None
        self.reference = Reference()
        self.phase = []

        if xml_node is not None:  # When should this ever be None?????
            self.id = xml_node.get('id')

            # UWS standard defines array, therefore treat phase as array
            # (... actually it does not, but keep it anyway like this, maybe at
            # some point in the future all phases of a job are provided as list)
            self.phase = [elm.text for elm in xml_node.findall(uws_flavour.phase)]
            self.reference = Reference(xml_node=xml_node, xml_namespace=xml_namespace)
            self.runId = xml_node.get('runId')
            self.ownerId = xml_node.get('ownerId')
            self.creationTime = xml_node.get('creationTime')

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
        if self.creationTime is not None:
            return "Job '%s' in phase '%s' created at '%s' - %s" % (self.id, ', '.join(self.phase), self.creationTime, unicode(self.reference))
        else:
            return "Job '%s' in phase '%s' - %s" % (self.id, ', '.join(self.phase), unicode(self.reference))

    def __str__(self):
        return unicode(self).encode('utf-8')


class Reference(BaseUWSModel):
    def __init__(self, href=None, type=None, xml_node=None, xml_namespace=None):
        super(Reference, self).__init__()

        self.type = "simple"
        self.href = ""

        if xml_node is not None:
            # check that namespace for xlink really exists
            if xlink_namespace not in xml_namespace.values():
                raise RuntimeError("No supported xlink namespace found in xml-response, cannot parse xml.")

            qualifiedname_type = et.QName(xlink_namespace, "type")
            qualifiedname_href = et.QName(xlink_namespace, "href")
            self.type = xml_node.get(qualifiedname_type)
            self.href = xml_node.get(qualifiedname_href)
        elif href is not None and type is not None:
            self.type = type
            self.href = href

    def __unicode__(self):
        return self.href

    def __str__(self):
        return unicode(self).encode('utf-8')


class Job(BaseUWSModel):
    def __init__(self, xml=None):
        super(Job, self).__init__()

        self.job_id = None
        self.run_id = None
        self.owner_id = None
        self.phase = ["PENDING"]
        self.quote = None
        self.creation_time = None
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
            uws_flavour = UWS1Flavour(parsed.nsmap)

            if parsed.get("version"):
                self.version = parsed.get("version")

            self.job_id        = self._get_mandatory(parsed, uws_flavour.jobId)
            self.run_id        = self._get_optional(parsed, uws_flavour.runId)
            self.owner_id      = self._get_optional(parsed, uws_flavour.ownerId)
            self.phase         = [self._get_mandatory(parsed, uws_flavour.phase)]
            self.quote         = self._get_optional(parsed, uws_flavour.quote)
            self.creation_time = self._get_optional(parsed, uws_flavour.creationTime)
            self.start_time    = self._get_mandatory(parsed, uws_flavour.startTime)
            self.end_time      = self._get_mandatory(parsed, uws_flavour.endTime)
            self.execution_duration = int(self._get_mandatory(parsed, uws_flavour.executionDuration))
            self.destruction   = self._get_mandatory(parsed, uws_flavour.destruction)

            self.parameters = []
            tmp = parsed.find(uws_flavour.parameters)
            if tmp is not None:
                parameters = list(tmp)
            for param in parameters:
                self.add_parameter(parameter=Parameter(xml_node=param))

            self.results = []
            tmp = parsed.find(uws_flavour.results)
            if tmp is not None:
                results = list(tmp)
            for res in results:
                self.add_result(result=Result(xml_node=res, xml_namespace=parsed.nsmap))

            self.error_summary = False
            tmp = parsed.find(uws_flavour.errorSummary)
            if tmp is not None:
                self.error_summary = ErrorSummary(xml_node=tmp, uws_flavour=uws_flavour)

            self.job_info = []
            tmp = parsed.find(uws_flavour.jobInfo)
            if tmp is not None:
                self.job_info = list(tmp)

    def __unicode__(self):
        str = "JobId : '%s'\n" % self.job_id
        str += "RunId : '%s'\n" % self.run_id
        str += "OwnerId : '%s'\n" % self.owner_id
        str += "Phase : '%s'\n" % ', '.join(self.phase)
        str += "Quote : '%s'\n" % self.quote
        str += "CreationTime : '%s'\n" % self.creation_time
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
        """Returns the text value of element_name within the parsed elementTree.

        If element_name doesn't exist, return None.
        """
        option = parsed.find(element_name)
        if option is None:
            return None
        else:
            return option.text

    def _get_mandatory(self, parsed, element_name):
        """Check if the element exists, return text or error"""

        element = parsed.find(element_name)
        if element is None:
            raise RuntimeError("Mandatory element ", element_name.text, " could not be found in xml-response.")
        else:
            return element.text


class Parameter(BaseUWSModel):
    def __init__(self, id=None, by_reference=False, is_post=False, value=None, xml_node=None):
        super(Parameter, self).__init__()

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
        super(Result, self).__init__()

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
                 xml_node=None, uws_flavour=None):
        super(ErrorSummary, self).__init__()

        self.type = "transient"
        self.has_detail = False
        self.messages = []

        if xml_node is not None:
            self.type = xml_node.get('type')
            self.has_detail = self._parse_bool(xml_node.get('hasDetail', default=False))

            self.messages = []
            messages = xml_node.findall(uws_flavour.message)

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

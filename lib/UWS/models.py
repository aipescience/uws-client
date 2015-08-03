from lxml import etree as et

UWSns = None


class jobs:
    __slots__ = ('jobref')

    def __init__(self, xml=None):
        if xml is not None:
            global UWSns

            #parse xml
            parsed = et.fromstring(xml)

            UWSns = parsed.nsmap

            xmlJobs = parsed.findall('uws:jobref', namespaces=UWSns)

            self.jobref = []
            for xmlJob in xmlJobs:
                self.addJob(job=jobref(xmlNode=xmlJob))

        else:
            self.jobref = []

    def __unicode__(self):
        str = ""
        for job in self.jobref:
            str += unicode(job) + "\n"
        return str

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return self.jobref

    def addJob(self, id=None, href=None, phase=None, job=None):
        if job is not None:
            self.jobref.append(job)
        else:
            currRef = reference(href=href, type="simple")
            currJobref = jobref(id=id, phase=phase, ref=currRef)
            self.jobref.append(currJobref)


class jobref:
    __slots__ = ('id', 'reference', 'phase')

    def __init__(self, id=None, phase=None, ref=None, xmlNode=None):
        if xmlNode is not None:
            self.id = xmlNode.get('id')

            #UWS standard defines array, therefore treat phase as array
            self.phase = [elm.text for elm in xmlNode.findall('uws:phase', namespaces=UWSns)]
            self.reference = reference(xmlNode=xmlNode)
        elif id is not None and phase is not None and ref is not None:
            self.id = id

            if isinstance(phase, basestring):
                self.phase = [phase]
            else:
                self.phase = phase

            if isinstance(ref, reference):
                self.reference = reference
            else:
                raise RuntimeError("Malformated reference given in jobref id: %s" % id)
        else:
            self.id = None
            self.phase = []
            self.reference = reference()

    def setPhase(self, newPhase):
        self.phase = [newPhase]

    def __unicode__(self):
        return "Job '%s' in phase '%s' - %s" % (self.id, ', '.join(self.phase), unicode(self.reference))

    def __str__(self):
        return unicode(self).encode('utf-8')


class reference:
    __slots__ = ('type', 'href')

    def __init__(self, href=None, type=None, xmlNode=None):
        if xmlNode is not None:
            self.type = xmlNode.get('{%s}type' % UWSns['xlink'])
            self.href = xmlNode.get('{%s}href' % UWSns['xlink'])
        elif href is not None and type is not None:
            self.type = type
            self.href = href
        else:
            self.type = "simple"
            self.href = ""

    def __unicode__(self):
        return self.href

    def __str__(self):
        return unicode(self).encode('utf-8')


class job:
    __slots__ = ('jobId', 'runId', 'ownerId', 'phase', 'quote', 'startTime', 'endTime',
                 'executionDuration', 'destruction', 'parameters', 'results', 'errorSummary',
                 'jobInfo')

    def __init__(self, xml=None):
        if xml is not None:
            global UWSns

            #parse xml
            parsed = et.fromstring(xml)

            UWSns = parsed.nsmap

            self.jobId = parsed.find('uws:jobId', namespaces=UWSns).text

            self.runId = self._getOptional(parsed, 'uws:runId')

            self.ownerId = parsed.find('uws:ownerId', namespaces=UWSns).text
            self.phase = [parsed.find('uws:phase', namespaces=UWSns).text]
            self.quote = self._getOptional(parsed, 'uws:quote')
            self.startTime = parsed.find('uws:startTime', namespaces=UWSns).text
            self.endTime = parsed.find('uws:endTime', namespaces=UWSns).text
            self.executionDuration = int(parsed.find('uws:executionDuration', namespaces=UWSns).text)
            self.destruction = parsed.find('uws:destruction', namespaces=UWSns).text

            self.parameters = []
            tmp = parsed.find('uws:parameters', namespaces=UWSns)
            if tmp is not None:
                parameters = list(tmp)
            for param in parameters:
                self.addParameter(parameter=parameter(xmlNode=param))

            self.results = []
            tmp = parsed.find('uws:results', namespaces=UWSns)
            if tmp is not None:
                results = list(tmp)
            for res in results:
                self.addResult(result=result(xmlNode=res))

                self.errorSummary = False
            tmp = parsed.find('uws:errorSummary', namespaces=UWSns)
            if tmp is not None:
                self.errorSummary = errorSummary(xmlNode=tmp)

            self.jobInfo = []
            tmp = parsed.find('uws:jobInfo', namespaces=UWSns)
            if tmp is not None:
                self.jobInfo = list(tmp)
        else:
            self.jobId = None
            self.runId = None
            self.ownerId = None
            self.phase = ["PENDING"]
            self.quote = None
            self.startTime = None
            self.endTime = None
            self.executionDuration = 0
            self.destruction = None
            self.parameters = []
            self.results = []
            self.errorSummary = None
            self.jobInfo = []

    def __unicode__(self):
        str = "JobId : '%s'\n" % self.jobId
        str += "RunId : '%s'\n" % self.runId
        str += "OwnerId : '%s'\n" % self.ownerId
        str += "Phase : '%s'\n" % ', '.join(self.phase)
        str += "Quote : '%s'\n" % self.quote
        str += "StartTime : '%s'\n" % self.startTime
        str += "EndTime : '%s'\n" % self.endTime
        str += "ExecutionDuration : '%s'\n" % self.executionDuration
        str += "Destruction : '%s'\n" % self.destruction

        str += "Parameters :\n"
        for param in self.parameters:
            str += "%s\n" % unicode(param)

        str += "Results :\n"
        for res in self.results:
            str += "%s\n" % unicode(res)

        str += "errorSummary :\n %s\n" % unicode(self.errorSummary)

        str += "jobInfo :\n"
        for info in self.jobInfo:
            str += "%s\n" % unicode(info)

        return str

    def __str__(self):
        return unicode(self).encode('utf-8')

    def addParameter(self, id=None, byReference=False, isPost=False, value=None, parameter=None):
        if parameter is not None:
            self.parameters.append(parameter)
        else:
            currParam = parameter(id=id, byReference=byReference, isPost=isPost, value=value)
            self.parameters.append(currParam)

    def addResult(self, id=None, href=None, result=None):
        if result is not None:
            self.results.append(result)
        else:
            currRef = reference(href=href, type="simple")
            currResult = result(id=id, ref=currRef)
            self.results.append(currResult)

    def _getOptional(self, parsed, elName):
        """returns the text value of elName within the elementTree
        parsed.

        If elName doesn't exist, this returns None.
        """
        mat = parsed.find(elName, namespaces=parsed.nsmap)
        if mat is None:
            return None
        else:
            return mat.text


class parameter:
    __slots__ = ('id', 'byReference', 'isPost', 'value')

    def __init__(self, id=None, byReference=False, isPost=False, value=None, xmlNode=None):
        if xmlNode is not None:
            self.id = xmlNode.get('id')
            self.byReference = xmlNode.get('byReference', default=False)
            self.isPost = xmlNode.get('isPost', default=False)
            self.value = xmlNode.text
        elif id is not None and value is not None:
            self.id = id
            self.byReference = byReference
            self.isPost = isPost
            self.value = value
        else:
            self.id = None
            self.byReference = False
            self.isPost = False
            self.value = None

    def __unicode__(self):
        return "Parameter id '%s' byRef: %s isPost: %s - value: %s" % (self.id, self.byReference, self.isPost, self.value)

    def __str__(self):
        return unicode(self).encode('utf-8')


class result:
    __slots__ = ('id', 'reference')

    def __init__(self, id=None, ref=None, xmlNode=None):
        if xmlNode is not None:
            self.id = xmlNode.get('id')
            self.reference = reference(xmlNode=xmlNode)
        elif id is not None and phase is not None and ref is not None:
            self.id = id

            if isinstance(ref, reference):
                self.reference = reference
            else:
                raise RuntimeError("Malformated reference given in result id: %s" % id)
        else:
            self.id = None
            self.reference = reference()

    def __unicode__(self):
        return "Result id '%s' reference: %s" % (self.id, unicode(self.reference))

    def __str__(self):
        return unicode(self).encode('utf-8')


class errorSummary:
    __slots__ = ('type', 'hasDetail', 'messages')

    def __init__(self, type="transient", hasDetail=False, messages=None, xmlNode=None):
        if xmlNode is not None:
            self.type = xmlNode.get('type')
            self.hasDetail = xmlNode.get('hasDetail', default=False)

            self.messages = []
            messages = xmlNode.findall('uws:message', namespaces=UWSns)
            for message in messages:
                self.messages.append(message.text)
        elif messages is not None:
            self.type = type
            self.hasDetail = hasDetail
            self.messages = messages
        else:
            self.type = "transient"
            self.hasDetail = False
            self.messages = []

    def __unicode__(self):
        return "Error Summary - type '%s' hasDetail: %s - message: %s" % (self.type, self.hasDetail, "\n".join(self.messages))

    def __str__(self):
        return unicode(self).encode('utf-8')

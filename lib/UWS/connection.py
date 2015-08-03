import httplib
import urllib
import urllib2
from urlparse import urlparse
import base64
import sys


class connection:
    def __init__(self, url, user=None, password=None):
        self._setURL(url)

        if user is not None and password is not None:
            self.authStr = base64.encodestring('%s:%s' % (user, password))
            self.authStr = self.authStr.replace('\n', '')
            self.headers = {"Authorization": "Basic %s" % self.authStr}
        else:
            self.headers = {}

        self.redirectCount = 0

    def _setURL(self, url):
        url = url.rstrip("/")
        urlParsed = urlparse(url)

        if urlParsed.scheme == '':
            urlParsed = urlparse("http://" + url)

        self.url = url
        self.cleanUrl = urlParsed.netloc
        self.basePath = urlParsed.path

        if urlParsed.scheme == "http":
            self.conn = httplib.HTTPConnection(self.cleanUrl)
        elif urlParsed.scheme == "https":
            self.conn = httplib.HTTPSConnection(self.cleanUrl)
        else:
            raise RuntimeError('Wrong protocol specified')

    def get(self, path):
        if(path == ""):
            self.conn.request("GET", self.basePath, headers=self.headers)
        else:
            self.conn.request("GET", self.basePath + '/' + path, headers=self.headers)

        res = self.conn.getresponse()

        if res.status == 302:
            #found - redirect
            location = res.getheader("location")
            newBasePath = location.replace(path, '').lstrip("/")
            self._setURL(newBasePath)

            self.redirectCount += 1
            if self.redirectCount > 100:
                raise RuntimeError("Too many redirects.")

            return self.get(path)

        if res.status == 400:
            raise RuntimeError('Resource responded with bad request')

        if res.status == 401:
            raise RuntimeError('You are not authorized to access this resource')

        if res.status == 403:
            raise RuntimeError('No permission to access this resource')

        if res.status == 404:
            raise RuntimeError('Resource does not exist')

        if res.status != 200:
            raise RuntimeError('Error while connection to server: Got response: %s %s' % (res.status, res.reason))

        return res

    def post(self, path, argDict):
        params = urllib.urlencode(argDict)

        if path:
          destURL = self.basePath + "/" + path
        else:
          destURL = self.basePath

        self.headers['Content-type'] = "application/x-www-form-urlencoded"
        self.conn.request("POST", destURL, body=params, headers=self.headers)
        res = self.conn.getresponse()
        res.read() # read body of request so we can send another

        if res.status == 302:
            #found - redirect
            location = res.getheader("location")
            newBasePath = location.replace(path, '').lstrip("/")
            self._setURL(newBasePath)

            self.redirectCount += 1
            if self.redirectCount > 100:
                raise RuntimeError("Too many redirects.")

            return self.post(path, argDict)

        if res.status == 303:
            #see other
            location = res.getheader("location")
            path = location.replace(self.url, '').lstrip('https://').lstrip('http://').lstrip("/")
            return self.get(path)

        if res.status == 400:
            raise RuntimeError('Resource responded with bad request')

        if res.status == 401:
            raise RuntimeError('You are not authorized to access this resource')

        if res.status == 403:
            raise RuntimeError('No permission to access this resource')

        if res.status == 404:
            raise RuntimeError('Resource does not exist')

        if res.status != 200:
            raise RuntimeError('Error while connection to server: Got response: %s %s' % (res.status, res.reason))

        return res

    def delete(self, path):
        self.conn.request("DELETE", self.basePath + '/' + path, headers=self.headers)
        res = self.conn.getresponse()
        res.read() # read body of request so we can send another

        if res.status == 302:
            #found - redirect
            location = res.getheader("location")
            newBasePath = location.replace(path, '').lstrip("/")
            self._setURL(newBasePath)

            self.redirectCount += 1
            if self.redirectCount > 100:
                raise RuntimeError("Too many redirects.")

            return self.delete(path)

        if res.status == 303:
            #see other
            location = res.getheader("location")
            path = location.replace(self.url, '').lstrip('https://').lstrip('http://').lstrip("/")
            return self.get(path)

        if res.status == 400:
            raise RuntimeError('Resource responded with bad request')

        if res.status == 401:
            raise RuntimeError('You are not authorized to access this resource')

        if res.status == 403:
            raise RuntimeError('No permission to access this resource')

        if res.status == 404:
            raise RuntimeError('Resource does not exist')

        if res.status != 200:
            raise RuntimeError('Error while connection to server: Got response: %s %s' % (res.status, res.reason))

        return res

    def downloadFile(self, url, usr, pwd, filename, chunkSizeKB=1024, callback=None):
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % self.authStr)
        handler = urllib2.urlopen(request)

        chunkSize = int(chunkSizeKB * 1024)

        if handler.headers.get('content-length') is not None:
            fileSize = handler.headers.get('content-length')
        else:
            fileSize = None

        #write the data to file
        fileRead = 0
        with open(filename, 'wb') as filePtr:
            for chunk in iter(lambda: handler.read(chunkSize), ''):
                fileRead += len(chunk)
                filePtr.write(chunk)

                if callback is not None:
                    callback(fileSize, fileRead)

        return True

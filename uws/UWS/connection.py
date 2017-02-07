# -*- coding: utf-8 -*-
try:
    import httplib
except ImportError:
    import http.client as httplib
try:
    import urllib2
    import urllib
    from urlparse import urlparse
except ImportError:
    import urllib.request as urllib2
    import urllib.parse as urllib
    from urllib.parse import urlparse
import base64


class Connection(object):
    def __init__(self, url, user=None, password=None):
        self._set_url(url)

        if user is not None and password is not None:
            try: 
                user = user.decode('utf-8')
                password = password.decode('utf-8')
            except AttributeError:
                pass
            auth_string = '%s:%s' % (user, password)
            self.auth_string = base64.encodestring(auth_string.encode())
            self.headers = {"Authorization":
                            ("Basic %s" %
                                self.auth_string.decode('utf-8')).strip('\n')}
        else:
            self.headers = {}

        self.redirect_count = 0

    def _set_url(self, url):
        url = url.rstrip("/")
        url_parsed = urlparse(url)

        if url_parsed.scheme == '':
            url_parsed = urlparse("http://" + url)

        self.url = url
        self.clean_url = url_parsed.netloc
        self.base_path = url_parsed.path

        if url_parsed.scheme == "http":
            self.connection = httplib.HTTPConnection(self.clean_url)
        elif url_parsed.scheme == "https":
            self.connection = httplib.HTTPSConnection(self.clean_url)
        else:
            raise RuntimeError('Wrong protocol specified')

    def get(self, path, params=None):

        if path:
            destination_url = self.base_path + "/" + path
        else:
            destination_url = self.base_path

        if params:
            params = urllib.urlencode(params, True)
            self.connection.request("GET", destination_url+'?'+params, headers=self.headers)
        else:
            self.connection.request("GET", destination_url, headers=self.headers)

        response = self.connection.getresponse()

        if response.status == 302 or response.status == 303:
            # found - redirect
            location = response.getheader("location")
            new_base_path = location.replace(path, '').lstrip("/")
            self._set_url(new_base_path)

            self.redirect_count += 1
            if self.redirect_count > 100:
                raise RuntimeError("Too many redirects.")

            return self.get(path)

        if response.status == 400:
            raise RuntimeError('Resource responded with bad request')

        if response.status == 401:
            raise RuntimeError('You are not authorized to access this resource')

        if response.status == 403:
            raise RuntimeError('No permission to access this resource')

        if response.status == 404:
            raise RuntimeError('Resource does not exist')

        if response.status != 200:
            raise RuntimeError('Error with connection to server: Got response: %s %s' % (response.status, response.reason))

        return response

    def post(self, path, args):
        params = urllib.urlencode(args)

        if path:
            destination_url = self.base_path + "/" + path
        else:
            destination_url = self.base_path

        self.headers['Content-type'] = "application/x-www-form-urlencoded"
        self.connection.request("POST", destination_url, body=params, headers=self.headers)
        response = self.connection.getresponse()
        response.read()  # read body of request so we can send another

        if response.status == 302:
            # found - redirect
            location = response.getheader("location")
            new_base_path = location.replace(path, '').lstrip("/")
            self._set_url(new_base_path)

            self.redirect_count += 1
            if self.redirect_count > 100:
                raise RuntimeError("Too many redirects.")

            return self.post(path, args)

        if response.status == 303:
            # see other
            location = response.getheader("location")
            path = location.replace(self.url, '').lstrip('https://').lstrip('http://').lstrip("/")
            return self.get(path)

        if response.status == 400:
            raise RuntimeError('Resource responded with bad request')

        if response.status == 401:
            raise RuntimeError('You are not authorized to access this resource')

        if response.status == 403:
            raise RuntimeError('No permission to access this resource')

        if response.status == 404:
            raise RuntimeError('Resource does not exist')

        if response.status != 200:
            raise RuntimeError('Error with connection to server: Got response: %s %s' % (response.status, response.reason))

        return response

    def delete(self, path):
        self.connection.request("DELETE", self.base_path + '/' + path, headers=self.headers)
        response = self.connection.getresponse()
        # read body of request so we can send another
        response.read()

        if response.status == 302:
            # found - redirect
            location = response.getheader("location")
            new_base_path = location.replace(path, '').lstrip("/")
            self._set_url(new_base_path)

            self.redirect_count += 1
            if self.redirect_count > 100:
                raise RuntimeError("Too many redirects.")

            return self.delete(path)

        if response.status == 303:
            # see other
            location = response.getheader("location")
            path = location.replace(self.url, '').lstrip('https://').lstrip('http://').lstrip("/")
            return self.get(path)

        if response.status == 400:
            raise RuntimeError('Resource responded with bad request')

        if response.status == 401:
            raise RuntimeError('You are not authorized to access this resource')

        if response.status == 403:
            raise RuntimeError('No permission to access this resource')

        if response.status == 404:
            raise RuntimeError('Resource does not exist')

        if response.status != 200:
            raise RuntimeError('Error with connection to server: Got response: %s %s' % (response.status, response.reason))

        return response

    def download_file(self, url, usr, pwd, file_name, chunk_size_kb=1024, callback=None):
        request = urllib2.Request(url)
        if hasattr(self, 'auth_string'):
            request.add_header("Authorization",
                               ("Basic %s" %
                                self.auth_string.decode('utf-8')).strip('\n'))
        handler = urllib2.urlopen(request)

        chunk_size = int(chunk_size_kb * 1024)

        if handler.headers.get('content-length') is not None:
            file_size = handler.headers.get('content-length')
        else:
            file_size = None

        # write the data to file
        file_read = 0
        with open(file_name, 'wb') as file_handler:
            for chunk in iter(lambda: handler.read(chunk_size), b''):
                file_read += len(chunk)
                file_handler.write(chunk)

                if callback is not None:
                    callback(file_size, file_read)

        return True

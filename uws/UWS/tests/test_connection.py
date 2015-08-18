# -*- coding: utf-8 -*-
import unittest

from uws import UWS


class ConnectionTest(unittest.TestCase):
    def testSetAuthHeader(self):
        connection = UWS.connection.Connection(
            "http://www.example.com/uws",
            user="admin",
            password="admin"
        )

        self.assertEqual(connection.auth_string, "YWRtaW46YWRtaW4=")
        self.assertDictEqual(connection.headers, {'Authorization': 'Basic YWRtaW46YWRtaW4='})

    def testSetURLHTTP(self):
        import httplib

        connection = UWS.connection.Connection(
            "http://www.example.com/uws/",
            user="admin",
            password="admin"
        )

        self.assertEqual(connection.url, "http://www.example.com/uws")
        self.assertEqual(connection.clean_url, "www.example.com")
        self.assertEqual(connection.base_path, "/uws")
        self.assertIsInstance(connection.connection, httplib.HTTPConnection)

    def testSetURLHTTPS(self):
        import httplib

        connection = UWS.connection.Connection(
            "https://www.example.com/uws/",
            user="admin",
            password="admin"
        )

        self.assertEqual(connection.url, "https://www.example.com/uws")
        self.assertEqual(connection.clean_url, "www.example.com")
        self.assertEqual(connection.base_path, "/uws")
        self.assertIsInstance(connection.connection, httplib.HTTPSConnection)

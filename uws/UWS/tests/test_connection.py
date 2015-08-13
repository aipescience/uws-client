import unittest

import uws.UWS.connection as UWSconnection


class ConnectionTest(unittest.TestCase):
    def testSetAuthHeader(self):
        conn = UWSconnection.connection(
            "http://www.example.com/uws",
            user="admin",
            password="admin"
        )

        self.assertEqual(conn.authStr, "YWRtaW46YWRtaW4=")
        self.assertDictEqual(conn.headers, {'Authorization': 'Basic YWRtaW46YWRtaW4='})

    def testSetURLHTTP(self):
        import httplib

        conn = UWSconnection.connection(
            "http://www.example.com/uws/",
            user="admin",
            password="admin"
        )

        self.assertEqual(conn.url, "http://www.example.com/uws")
        self.assertEqual(conn.cleanUrl, "www.example.com")
        self.assertEqual(conn.basePath, "/uws")
        self.assertIsInstance(conn.conn, httplib.HTTPConnection)

    def testSetURLHTTPS(self):
        import httplib

        conn = UWSconnection.connection(
            "https://www.example.com/uws/",
            user="admin",
            password="admin"
        )

        self.assertEqual(conn.url, "https://www.example.com/uws")
        self.assertEqual(conn.cleanUrl, "www.example.com")
        self.assertEqual(conn.basePath, "/uws")
        self.assertIsInstance(conn.conn, httplib.HTTPSConnection)


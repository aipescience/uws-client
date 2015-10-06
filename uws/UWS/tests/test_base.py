# -*- coding: utf-8 -*-
import unittest

from uws import UWS


class BaseTest(unittest.TestCase):
    def testValidateAndParsePhaseFilter(self):
        filters = {
            'phases': ['COMPLETED', 'PENDING']
        }

        params = UWS.client.Client("/")._validate_and_parse_filters(filters)

        self.assertEqual(params, [('PHASE','COMPLETED'), ('PHASE','PENDING')])

    def testValidateAndParsePhaseFilterInvalidPhase(self):
        filters = {
            'phases': ['FOO', 'PENDING']
        }

        self.assertRaises(
            UWS.UWSError,
            UWS.client.Client("/")._validate_and_parse_filters,
            filters
        )

    def testValidateAndParseAfterFilter(self):
        filters = {
            'after': '2015-09-10T10:01:02.135'
        }

        params = UWS.base.BaseUWSClient(None)._validate_and_parse_filters(filters)

        self.assertEqual(params, [('AFTER','2015-09-10T10:01:02.135000')])

    def testValidateAndParseAfterFilterInvalidDate(self):
        filters = {
            'after': '2010-4--'
        }

        self.assertRaises(
            UWS.UWSError,
            UWS.base.BaseUWSClient(None)._validate_and_parse_filters,
            filters
        )

    def testValidateAndParseLastFilter(self):
        filters = {
            'last': '1000'
        }

        params = UWS.base.BaseUWSClient(None)._validate_and_parse_filters(filters)

        self.assertEqual(params, [('LAST',1000)])

    def testValidateAndParseLastFilterFloatValue(self):
        filters = {
            'last': '100.0'
        }

        self.assertRaises(UWS.UWSError, UWS.base.BaseUWSClient(None)._validate_and_parse_filters, filters)

    def testValidateAndParseLastFilterNegativeValue(self):
        filters = {
            'last': '-100'
        }

        self.assertRaises(UWS.UWSError, UWS.base.BaseUWSClient(None)._validate_and_parse_filters, filters)

    def testValidateAndParseAfterLastFilter(self):
        filters = {
            'after': '2015-09-10T10:01:02.135',
            'last': '100'
        }

        params = UWS.base.BaseUWSClient(None)._validate_and_parse_filters(filters)

        self.assertEqual(params, [('AFTER','2015-09-10T10:01:02.135000'), ('LAST', 100)])

    def testValidateAndParseAfterLastPhaseFilter(self):
        filters = {
            'after': '2015-09-10T10:01:02.135',
            'last': '100',
            'phases': ['PENDING', 'ERROR']
        }

        params = UWS.base.BaseUWSClient(None)._validate_and_parse_filters(filters)

        self.assertEqual(params, [ ('PHASE','PENDING'), ('PHASE','ERROR'), ('AFTER','2015-09-10T10:01:02.135000'), ('LAST', 100)])


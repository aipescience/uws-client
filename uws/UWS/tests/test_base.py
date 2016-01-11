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

        params = UWS.client.Client("/")._validate_and_parse_filters(filters)

        self.assertEqual(params, [('AFTER','2015-09-10T10:01:02.135000')])

    def testValidateAndParseAfterFilterInvalidDate(self):
        filters = {
            'after': '2010-4--'
        }

        self.assertRaises(
            UWS.UWSError,
            UWS.client.Client("/")._validate_and_parse_filters,
            filters
        )

    def testValidateAndParseAfterFilterTimeZone(self):
        filters = {
            'after': '2015-10-03T01:12+2:00'
        }

        params = UWS.client.Client("/")._validate_and_parse_filters(filters)

        self.assertEqual(params, [('AFTER', '2015-10-02T23:12:00')])



    def testValidateAndParseLastFilter(self):
        filters = {
            'last': '1000'
        }

        params = UWS.client.Client("/")._validate_and_parse_filters(filters)

        self.assertEqual(params, [('LAST',1000)])

    def testValidateAndParseLastFilterFloatValue(self):
        filters = {
            'last': '100.0'
        }

        self.assertRaises(
            UWS.UWSError,
            UWS.client.Client("/")._validate_and_parse_filters,
            filters
        )

    def testValidateAndParseLastFilterNegativeValue(self):
        filters = {
            'last': '-100'
        }

        self.assertRaises(
            UWS.UWSError,
            UWS.client.Client("/")._validate_and_parse_filters,
            filters
        )

    def testValidateAndParseAfterLastFilter(self):
        filters = {
            'after': '2015-09-10T10:01:02.135',
            'last': '100'
        }

        params = UWS.client.Client("/")._validate_and_parse_filters(filters)

        self.assertEqual(params, [('AFTER','2015-09-10T10:01:02.135000'),
            ('LAST', 100)])

    def testValidateAndParseAfterLastPhaseFilter(self):
        filters = {
            'after': '2015-09-10T10:01:02.135',
            'last': '100',
            'phases': ['PENDING', 'ERROR']
        }

        params = UWS.client.Client("/")._validate_and_parse_filters(filters)

        self.assertEqual(params, [ ('PHASE','PENDING'), ('PHASE','ERROR'),
            ('AFTER','2015-09-10T10:01:02.135000'), ('LAST', 100)])

    def testValidateAndParseWaitNegative(self):
        wait = '-1'
        params = UWS.client.Client("/")._validate_and_parse_wait(wait)

        self.assertEqual(params, [('WAIT', -1)])

    def testValidateAndParseWait(self):
        wait = '30'
        params = UWS.client.Client("/")._validate_and_parse_wait(wait)

        self.assertEqual(params, [('WAIT', 30)])

    def testValidateAndParseWaitInvalidWait(self):
        wait = '30.587'

        self.assertRaises(
            UWS.UWSError,
            UWS.client.Client("/")._validate_and_parse_wait,
            wait
        )

    def testValidateAndParseWaitInvalidWaitNegative(self):
        wait = '-30'

        self.assertRaises(
            UWS.UWSError,
            UWS.client.Client("/")._validate_and_parse_wait,
            wait
        )

    def testValidateAndParseWaitPhase(self):
        wait = '30'
        phase = 'EXECUTING'

        params = UWS.client.Client("/")._validate_and_parse_wait(wait, phase)

        self.assertEqual(params, [('WAIT', 30), ('PHASE', 'EXECUTING')])

    def testValidateAndParseWaitInvalidPhase(self):
        wait = '15'
        phase = 'COMPLETED'

        self.assertRaises(
            UWS.UWSError,
            UWS.client.Client("/")._validate_and_parse_wait,
            wait, phase
        )

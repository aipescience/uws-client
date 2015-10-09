# -*- coding: utf-8 -*-
import unittest

from uws import UWS


class BaseTest(unittest.TestCase):
    def testValidateAndParseFilter(self):
        filters = {
            'phases': ['COMPLETED', 'PENDING']
        }

        params = UWS.client.Client("/")._validate_and_parse_filters(filters)

        self.assertEqual(params, [('PHASE','COMPLETED'), ('PHASE','PENDING')])

    def testValidateAndParseFilterInvalidPhase(self):
        filters = {
            'phases': ['FOO', 'PENDING']
        }

        self.assertRaises(
            UWS.UWSError,
            UWS.client.Client("/")._validate_and_parse_filters,
            filters
        )

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

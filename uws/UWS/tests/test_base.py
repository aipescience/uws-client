# -*- coding: utf-8 -*-
import unittest

from uws import UWS


class BaseTest(unittest.TestCase):
    def testValidateAndParseFilter(self):
        filters = {
            'phases': ['COMPLETED', 'PENDING']
        }

        params = UWS.base.BaseUWSClient(None)._validate_and_parse_filters(filters)

        self.assertEqual(params, [('PHASE','COMPLETED'), ('PHASE','PENDING')])

    def testValidateAndParseFilterInvalidPhase(self):
        filters = {
            'phases': ['FOO', 'PENDING']
        }

        self.assertRaises(
            UWS.UWSError,
            UWS.base.BaseUWSClient(None)._validate_and_parse_filters,
            filters
        )
import os
import curart
import unittest

class CurartTestCase(unittest.TestCase):

    def setUp(self):
        curart.app.testing = True
        self.app = curart.app.test_client()

    def test_home_page(self):
        rv = self.app.get('/')
        assert rv.status_code == 200


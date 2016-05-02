# coding: utf-8
import os
import sys
import plistlib
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))
from iOSprofile import mprofile, serve
import unittest

class TestConfMaker(unittest.TestCase):
    def setUp(self):
        self.invhost = 32
        self.host = 'scj643'
        self.url = 'http://google.com'
    
    def test_conf_str(self):
        mprofile.Config(self.host)
    
    def test_conf_unicode(self):
        mprofile.Config(unicode(self.host))
    
    def test_conf_invalid(self):
        with self.assertRaises(mprofile.ParamInvalid):
            mprofile.Config(self.invhost)
            

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConfMaker)
unittest.TextTestRunner(verbosity=2).run(suite)

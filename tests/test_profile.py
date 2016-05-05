# coding: utf-8
import os
import sys
import pytest
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))
from iOSprofile import mprofile, serve


invhost = 32
host = 'scj643'
url = 'http://google.com'
    
def test_conf_str():
    mprofile.Config(host)


def test_conf_unicode():
    mprofile.Config(unicode(host))


def test_conf_invalid():
    with pytest.raises(mprofile.ParamInvalid):
        mprofile.Config(invhost)
            


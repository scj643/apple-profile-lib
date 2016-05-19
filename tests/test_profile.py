# coding: utf-8
import os
import sys
import pytest
if sys.version_info[0]<=3:
    unicode = str
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))
from iOSprofile import mprofile, serve


invhost = 32
host = 'test'

    
def test_conf_str():
    mprofile.Config(host)


def test_conf_unicode():
    mprofile.Config(unicode(host))


def test_conf_invalid():
    with pytest.raises(mprofile.ParamInvalid):
        mprofile.Config(invhost)
            
def test_missing_args():
    with pytest.raises(TypeError):
        mprofile.Config()

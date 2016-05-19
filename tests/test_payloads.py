# coding: utf-8
import os
import sys
import pytest
if sys.version_info[0] <= 3:
    unicode = str
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))
from iOSprofile import mprofile, serve


invdata = b'test'
title = 'Test Title'
organization = 'Test Organiztion'
domain = 'com'
name = 'Test Name'
description = 'A test profile/payload'
host = 'test'
url = 'http://google.com'
identity = 'test'

config = mprofile.Config(host, identity, domain, description, 
                         name, organization)


def test_payload():
    global payload
    payload = mprofile.Payloads(config)


def test_webclip():
    payload.webclip(url, 'test', ident=identity, horg=organization,
                    hname='Webclip Test', hdesc='A webclip')

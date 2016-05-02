# coding: utf-8
import plistlib
import uuid
from datetime import datetime
from io import BytesIO

try:
    import Crypto

    Crypto_support = True
except ImportError:
    Crypto_support = False
    print 'No crypto support'
try:
    import biplist

    binary_support = True
except ImportError:
    binary_support = False
    print 'No binary support'
try:
    import PIL

    imgsupport = True
except ImportError:
    imgsupport = False
    print('No PIL support')
if imgsupport:
    from PIL import Image


# Defining Exceptions
class ParamInvalid(Exception):
    """Exception raised for invalid param type.

    Attributes:
        atrib -- paramater missing
    """

    def __init__(self, atrib, etype):
        self.atrib = atrib
        self.etype = etype

    def __str__(self):
        return 'Argument ' + repr(self.atrib) + ' is wrong type should be ' + repr(self.etype)


def typehandle(value, argn, opt=True, rtype=str):
    """Handles verifying type checks

    :param value: The value to be checked
    :param argn: The name of the argument to pass if an exception occurs
    :param opt: Bool if the variable is optional
    :param rtype: Type that the value should be (Defaults to str/unicode)
    :return: Value if success, ParamInvalid if failed
    """
    if opt and isinstance(value, type(None)):
        return
    if rtype == str:
        rtype = [str, unicode]
    if isinstance(rtype, list):
        for i in rtype:
            if isinstance(value, i):
                return value
        else:
            raise ParamInvalid(argn, rtype)
    else:
        if isinstance(value, rtype):
            return value
        else:
            raise ParamInvalid(argn, rtype)


def strip(indict):
    """Strips keys with a value of None from a dict

    :param indict: Dictionary to be striped
    :return: Striped dictionary
    """
    outdict = {k: v for k, v in indict.items() if v is not None}
    return outdict


def uid():
    return uuid.uuid4().urn[9:].upper()


class Config(object):
    def __init__(self, host, ident=uid(), domain='org', hdesc=None, hname=None, horg=None,
                 rdate=None):
        self.host = typehandle(host, 'host', False)
        self.domain = typehandle(domain, 'domain')
        self.hdesc = typehandle(hdesc, 'hdesc')
        self.hname = typehandle(hname, 'hname')
        self.horg = typehandle(horg, 'horg')
        self.rdate = rdate
        self.rdn = domain + '.' + host
        self.ident = self.rdn + '.' + ident


class Payloads(object):
    def __init__(self, config):
        # noinspection PyTypeChecker
        self.config = typehandle(config, 'comfig', False, Config)
        self.profile = []

    def font(self, font, ident=uid(), name=None, **kwargs):
        ident = 'font.' + ident
        returns = {'PayloadType': 'com.apple.font'}
        if font:
            returns['Font'] = plistlib.Data(font)
        else:
            return
        returns['Name'] = typehandle(name, 'name')
        returns = self.common(returns, ident, kwargs)
        striped = strip(returns)
        self.profile += [striped]

    def webclip(self, url, label, fullscreen=None, ident=uid(), icon=None,
                precomposed=True, removable=True, **kwargs):
        ident = 'webclip.' + ident
        returns = {'PayloadType': 'com.apple.webClip.managed', 'URL': url,
                   'Label': label, 'IsRemovable': removable}
        if icon and imgsupport:
            if type(icon) == str:
                img = Image.open(icon)
            else:
                img = icon
            data_buffer = BytesIO()
            img.save(data_buffer, 'PNG')
            icon_data = data_buffer.getvalue()
            returns['Icon'] = plistlib.Data(icon_data)
        returns['Precomposed'] = typehandle(precomposed, 'precomposed', rtype=bool)
        returns['FullScreen'] = typehandle(fullscreen, 'fullscreen', rtype=bool)
        returns = self.common(returns, ident, kwargs)
        striped = strip(returns)
        self.profile += [striped]

    def vpn(self, vpntype, alltraffic=False):
        return

    def certificate(self, certtype, cert, filename=None, password=None, ident=uid(), **kwargs):
        returns = {}
        if ['root', 'pkcs1', 'pem', 'pkcs12'].__contains__(certtype):
            returns['PayloadType'] = 'com.apple.security.' + certtype
        else:
            return
        if cert:
            returns['PayloadContent'] = plistlib.Data(cert)
        else:
            return
        returns['PayloadCertificateFilename'] = typehandle(filename, 'filename')
        returns['Password'] = typehandle(password, 'password')
        returns = self.common(returns, ident, kwargs)
        striped = strip(returns)
        self.profile += [striped]

    def wifi(self, ssid, hidden=False, encryption='Any', hotspot=False, autojoin=True,
             pw=None, ident=uid(), **kwargs):
        ident = 'wifi.' + ident
        returns = {'PayloadType': 'com.apple.wifi.managed'}
        returns['SSID_STR'] = typehandle(ssid, 'ssid', rtype=bool)
        returns['HIDDEN_NETWORK'] = typehandle(hidden, 'hidden', rtype=bool)
        returns['AutoJoin'] = typehandle(autojoin, 'autojoim', rtype=bool)
        if encryption in ['WEP', 'WPA', 'WPA2', 'Any', 'None']:
            returns['EncryptionType'] = encryption
        returns['Password'] = typehandle(pw, 'password')
        returns = self.common(returns, ident, kwargs)
        striped = strip(returns)
        self.profile += [striped]

    def common(self, content, ident, horg=None, hname=None, hdesc=None, ver=1):
        content['PayloadIdentifier'] = self.config.ident + '.' + ident
        content['PayloadOrganization'] = typehandle(horg, 'horg', )
        content['PayloadDisplayName'] = typehandle(hname, 'hname')
        content['PayloadDescription'] = typehandle(hdesc, 'hdesc')
        content['title'] = self.config.ident + '.' + ident
        content['PayloadUUID'] = uid()
        content['PayloadVersion'] = ver
        return content


def strippayload(payloads):
    # remove title attribute from payloads
    for i in payloads.profile:
        if 'title' in i:
            del i['title']
    return payloads


def mkplist(pload):
    """Turns a Payloads object into a plist

    :param pload: The Payloads object
    :return: Dict representation of plist
    """
    p = strippayload(pload)
    returns = {'PayloadType': 'Configuration', 'PayloadVersion': 1,
               'PayloadIdentifier': pload.config.ident,
               'PayloadUUID': uid()}

    returns['PayloadDescription'] = typehandle(pload.config.hdesc, 'hdesc')
    returns['PayloadDisplayName'] = typehandle(pload.config.hname, 'hdesc')
    returns['PayloadOrganization'] = typehandle(pload.config.horg, 'horg')
    if pload.config.rdate:
        returns['RemovalDate'] = pload.config.rdate
    returns['PayloadContent'] = pload.profile
    return returns
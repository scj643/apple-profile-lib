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
    print('No crypto support')
try:
    import biplist
    binary_support = True
except ImportError:
    binary_support = False
    print('No binary support')
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
        return 'Argument ' + repr(self.atrib) +' is wrong type should be ' + repr(self.etype)


def typehandle(value, argn, opt=True, rtype=str):
    """Helper for handling argument verification

    Attributes:
        value -- value to be tested
        argn  -- name of argument
        opt   -- is value option
        rtype -- type to be matched to (can be list of types or just a type)
    """
    if type(value) == rtype:
        return value
    elif type(value) == type(None) and opt:
        return value
    else:
        raise ParamInvalid(argn, rtype)


def uid():
    return uuid.uuid4().urn[9:].upper()


class Config(object):
    def __init__(self, host, ident=uid(), domain='org', hdesc=None, hname=None, horg=None,
                 rdate=None):
        self.host = typehandle(host,'host',False)
        self.domain = typehandle(domain,'domain')
        self.hdesc = typehandle(hdesc,'hdesc')
        self.hname = typehandle(hname,'hname')
        self.horg = typehandle(horg,'horg')
        self.rdate = rdate
        self.rdn = domain + '.' + host
        self.ident = self.rdn + '.' + ident


class Payloads(object):
    def __init__(self, config):
        self.config = typehandle(config,'comfig',False,type(Config('t')))
        self.profile = list()

    def font(self, font, ident=uid(), name=None, **kwargs):
        ident = 'font.'+ ident
        returns = {'PayloadType': 'com.apple.font'}
        if font:
            returns['Font'] = plistlib.Data(font)
        else:
            return
        returns['Name'] = typehandle(name,'name')
        returns = self.common(returns, ident, kwargs)
        self.profile += list(returns)

    def webclip(self, url, label, fullscreen=None, ident=uid(), icon=None,
                precomposed=True, removable=True, **kwargs):
        ident = 'webclip.'+ident
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
        returns['Precomposed'] = typehandle(precomposed,'precomposed',rtype=bool)
        returns['FullScreen'] = typehandle(fullscreen,'fullscreen',rtype=bool)
        returns = self.common(returns, ident, kwargs)
        self.profile += [returns]

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
        returns['PayloadCertificateFilename'] = typehandle(filename,'filename')
        returns['Password'] = typehandle(password,'password')
        returns = self.common(returns, ident, kwargs)
        self.profile += [returns]
    
    def wifi(self, ssid, hidden = False, encryption = 'Any', hotspot = False, autojoin = True,
             pw = None, ident = uid(), **kwargs):
        ident = 'wifi.'+ident
        returns = {'PayloadType': 'com.apple.wifi.managed'}
        returns['SSID_STR'] = typehandle(ssid,'ssid',rtype=bool)
        returns['HIDDEN_NETWORK'] = typehandle(hidden,'hidden',rtype=bool)
        returns['AutoJoin'] = typehandle(autojoin,'autojoim',rtype=bool)
        if ['WEP', 'WPA', 'WPA2', 'Any', 'None'].__contains__(encryption):
            returns['EncryptionType'] = encryption
        returns['Password'] = typehandle(pw, 'password')
        returns = self.common(returns, ident, kwargs)
        self.profile += [returns]

    def common(self, content, ident, horg=None, hname=None, hdesc=None, ver=1):
        content['PayloadIdentifier'] = self.config.ident + '.' + ident
        content['PayloadOrganization'] = typehandle(horg,'horg')
        content['PayloadDisplayName'] = typehandle(hname,'hname')
        content['PayloadDescription'] = typehandle(hdesc,'hdesc')
        content['title'] = self.config.ident + '.' + ident
        content['PayloadUUID'] = uid()
        content['PayloadVersion'] = ver
        return content

def strippayload(payloads):
    # remove title atribute from payloads
    for i in payloads.profile:
        if i.has_key('title'):
            i.__delitem__('title')
    return payloads

def mkplist(pload):
    '''
    pload: a Payloads object
    '''
    p = strippayload(pload)
    returns = {'PayloadType': 'Configuration', 'PayloadVersion': 1,
               'PayloadIdentifier': pload.config.ident,
               'PayloadUUID': uid()}
    
    returns['PayloadDescription'] = typehandle(pload.config.hdesc,'hdesc')
    returns['PayloadDisplayName'] = typehandle(pload.config.hname,'hdesc')
    returns['PayloadOrganization'] = typehandle(pload.config.horg,'horg')
    if pload.config.rdate:
        returns['RemovalDate'] = pload.config.rdate
    returns['PayloadContent'] = pload.profile
    return returns
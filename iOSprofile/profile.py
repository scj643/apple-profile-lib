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

def uid():
    return uuid.uuid4().urn[9:].upper()


class Config(object):
    def __init__(self, host, ident=uid(), domain='org', hdesc=None, hname=None, horg=None,
                 rdate=None):
        self.host = host
        self.domain = domain
        self.hdesc = hdesc
        self.hname = hname
        self.horg = horg
        self.rdate = rdate
        self.rdn = domain + '.' + host
        self.ident = self.rdn + '.' + ident


class Payloads(object):
    def __init__(self, config):
        self.config = config
        self.profile = list()

    def font(self, font, ident=uid(), name=None, **kwargs):
        ident = 'font.'+ ident
        returns = {'Font': plistlib.Data(font),
                   'PayloadIdentifier': self.config.rdomain + id,
                   'PayloadType': 'com.apple.font'}
        if type(name) == str:
            returns['Name'] = name
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
        if type(precomposed) == bool:
            returns['Precomposed'] = precomposed
        if type(fullscreen) == bool:
            returns['FullScreen'] = fullscreen
        returns = self.common(returns, ident, kwargs)
        self.profile += [returns]

    def vpn(self, vpntype, alltraffic=False):
        return
    
    def wifi(self, ssid, hidden = False, encryption = 'Any', hotspot = False, autojoin = True,
             pw = None, ident = uid(), **kwargs):
        ident = 'wifi.'+ident
        returns = {'PayloadType': 'com.apple.wifi.managed'}
        if type(ssid) == str:
            returns['SSID_STR'] = ssid
        if type(hidden) == bool:
            returns['HIDDEN_NETWORK'] = hidden
        if type(autojoin) == bool:
            returns['AutoJoin'] = autojoin
        if ['WEP', 'WPA', 'WPA2', 'Any', 'None'].__contains__(encryption):
            returns['EncryptionType'] = encryption
        if type(pw) == str:
            returns['Password'] = pw
        returns = self.common(returns, ident, kwargs)
        self.profile += [returns]

    def common(self, content, ident, horg=None, hname=None, hdesc=None, ver=1):
        content['PayloadIdentifier'] = self.config.ident + '.' + ident
        if type(horg) == str:
            content['PayloadOrganization'] = horg
        if type(hname) == str:
            content['PayloadDisplayName'] = hname
        if type(hdesc) == str:
            content['PayloadDescription'] = hdesc
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

def mkplist(config, ploads):
    p = strippayload(ploads)
    returns = {'PayloadType': 'Configuration', 'PayloadVersion': 1,
               'PayloadIdentifier': config.ident,
               'PayloadUUID': uid()}
    if type(config.hdesc) == str:
        returns['PayloadDescription'] = config.hdesc
    if type(config.hname) == str:
        returns['PayloadDisplayName'] = config.hname
    if type(config.horg) == str:
        returns['PayloadOrganization'] = config.horg
    if type(config.rdate) == datetime:
        returns['RemovalDate'] = config.rdate
    returns['PayloadContent'] = p.profile
    return returns
# coding: utf-8
import plistlib
import uuid
from datetime import datetime



def uid():
    return uuid.uuid4().urn[9:].upper()


class config (object):
    def __init__(self, host, ident=uid(), domain='org'):
        self.host = host
        self.domain = domain
        self.rdn = domain + '.' + host
        self.ident = self.rdn + '.' + ident

class payloads(config):
    def __init__(self,config):
        self.config = config
        self.profile = list()
    

    def font(self,font,ident=uid(),name=None,**kwargs):
        returns = {'Font':plistlib.Data(font),
        'PayloadIdentifier':self.config.rdomain+id,
        'PayloadType':'com.apple.font'}
        if type(name) == str:
            returns['Name'] = name
        returns = self.common(returns,ident,kwargs)
        self.profile += list(returns)


    def webclip(self,url,label,fullscreen=None,ident=uid(),icon=None,
                precomposed=True,removable=True,**kwargs):
        returns = {'PayloadType': 'com.apple.webClip.managed', 'URL': url,
                   'Label': label, 'IsRemovable': removable}
        if icon:
            returns['Icon']=plistlib.Data(icon)
        if type(precomposed) == bool:
            returns['Precomposed']=precomposed
        if type(fullscreen) == bool:
            returns['FullScreen']=fullscreen
        returns = self.common(returns, ident, kwargs)
        print returns
        self.profile += [returns]
        
    
    def vpn(name,vtype,alltraffic=False):
        return

    def common(self,content,ident,horg=None,hname=None,hdisc=None,ver=1):
        content['PayloadIdentifier']=self.config.ident + '.' + ident
        if type(horg) == str:
            content['PayloadOrganization']=horg
        if type(hname) == str:
            content['PayloadDisplayName']=hname
        if type(hdisc) == str:
            content['PayloadDescription']=hdisc
        content['PayloadUUID']=uid()
        content['PayloadVersion']=ver
        return content


def mkplist(payloadc,hdesc=None, hname=None, horg=None,rdate=None):
    returns = {'PayloadType': 'Configuration','PayloadVersion': 1,
               'PayloadIdentifier': payloadc.config.ident,
               'PayloadUUID': uid()}
    if type(hdesc) == str:
        returns['PayloadDescription'] = hdesc
    if type(hname) == str:
        returns['PayloadDisplayName'] = hname
    if type(horg) == str:
        returns['PayloadOrganization'] = horg
    if type(rdate) == datetime :
        returns['RemovalDate'] = rdate
    returns['PayloadContent']=payloadc.profile
    return returns

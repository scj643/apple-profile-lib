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
        if name:
            returns['Name']=str(name)
        returns = self.common(returns,ident,kwargs)
        self.profile += list(returns)
        
    def webclip(self,url,label,fullscreen=None,ident=uid(),icon=None,
                precomposed=True,removable=True,**kwargs):
        returns = {'PayloadType': 'com.apple.webClip.managed', 'URL': url,
                   'Label': label, 'IsRemovable': removable}
        if icon:
            returns['Icon']=plistlib.Data(icon)
        if precomposed:
            returns['Precomposed']=precomposed
        if fullscreen:
            returns['FullScreen']=fullscreen
        returns = self.common(returns, ident, kwargs)
        print returns
        self.profile += [returns]
        
    def common(self,content,ident,horg=None,hname=None,hdisc=None,ver=1):
        content['PayloadIdentifier']=self.config.ident + '.' + ident
        if horg:
            content['PayloadOrganization']=horg
        if hname:
            content['PayloadDisplayName']=hname
        if hdisc:
            content['PayloadDescription']=hdisc
        content['PayloadUUID']=uid()
        content['PayloadVersion']=ver
        return content
        

def mkplist(payloads,hdesc=None, hname=None, horg=None,rdate=None):
    returns = {'PayloadType': 'Configuration','PayloadVersion': 1,
               'PayloadIdentifier': payloads.config.ident,
               'PayloadUUID': uid()}
    if hdesc:
        returns['PayloadDescription'] = hdesc
    if hname:
        returns['PayloadDisplayName'] = hname
    if horg:
        returns['PayloadOrganization'] = horg
    returns['PayloadContent']=payloads.profile
    return returns
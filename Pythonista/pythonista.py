# coding: utf-8
import os
import sys
import dialogs
import ui
import photos
import plistlib
ROOT_PATH = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))
from iOSprofile import profile, serve

common_form = [{'title':'Ident', 'type':'text', 'autocorrection':False,
          'autocapitalization':ui.AUTOCAPITALIZE_NONE,'key':'ident'},
         {'title':'Description', 'type':'text', 'autocorrection':True, 'key':'hdesc'},
         {'title':'Organization', 'type':'text', 'autocorrection':False,
          'autocapitalization':ui.AUTOCAPITALIZE_NONE,'key':'horg'},
         {'title':'Name', 'type':'text', 'autocorrection':False,
          'autocapitalization':ui.AUTOCAPITALIZE_NONE, 'key':'hname'}]

def webclip(payload):
    form = [{'title':'URL','type':'url','key':'url'},
            {'title':'Title','key':'label','type':'text'},
            {'title':'Removable','key':'removable','type':'switch','value':True},
            {'title':'Fullscreen','key':'fullscreen','type':'switch','value':False},
            {'title':'Precomposed','key':'precomposed','type':'switch','value':True},
            {'title':'image','key':'icon','type':'switch','value':False}] + common_form
    returns = dialogs.form_dialog('Webclip',form)
    image = None
    if returns['icon']:
        returns['icon'] = photos.pick_image(True)
    if returns:
        payload.webclip(**returns)

def wifi(payload):
    form = [{'title':'ssid', 'type':'text', 'key':'ssid', 'autocorrection':False,
             'autocapitalization':ui.AUTOCAPITALIZE_NONE},
            {'title':'Hidden', 'key':'hidden', 'type':'switch', 'valie':True},
            {'title':'Autojpin', 'key':'autojoin', 'type':'switch', 'valie':True},
            {'title':'Hotspot', 'key':'hotspot', 'type':'switch', 'valie':False},
            {'title':'Encryption type', 'key':'encryption', 'type':'text', 'autocorrection':False},
            {'title':'Password', 'key':'pw', 'type':'password'}] + common_form
    returns = dialogs.form_dialog('Wifi',form)
    if returns:
        payload.webclip(**returns)

def setup():
    d = [{'title':'Host', 'type':'text','autocorrection':False,
          'autocapitalization':ui.AUTOCAPITALIZE_NONE,'key':'host'},
         {'title':'Domain', 'type':'text', 'autocorrection':False, 'autocapitalization':ui.AUTOCAPITALIZE_NONE,'placeholder':'org','key':'domain'},
         {'title':'Ident', 'type':'text', 'autocorrection':False,
          'autocapitalization':ui.AUTOCAPITALIZE_NONE,'key':'ident'},
         {'title':'Description', 'type':'text', 'autocorrection':True, 'key':'hdesc'},
         {'title':'Organization', 'type':'text', 'autocorrection':False,
          'autocapitalization':ui.AUTOCAPITALIZE_NONE,'key':'horg'},
         {'title':'Name', 'type':'text', 'autocorrection':False,
          'autocapitalization':ui.AUTOCAPITALIZE_NONE, 'key':'hname'}]
    r = dialogs.form_dialog('Setup',d)
    if r == None:
        print 'Canceled'
        return
    # remove keys with empty values
    for i in r:
        if r[i] == '':
            r.pop(i)
    # Check to make sure we got a host name
    if 'host' in r:
        return r
    print 'No host name'
    return None

def editpayload(payload):
    editing = True
    while editing:
        mainops = [{'title':'Edit'},{'title':'Add Webclip'},{'title':'Add Wifi'},{'title':'Serve'},{'title':'Save'}]+payload.profile
        choice = dialogs.list_dialog('Profile',mainops)
        if choice == None:
            editing == False
        if choice['title'] == 'Edit':
            payload.profile = dialogs.edit_list_dialog('Edit Profiles', payload.profile)
        if choice['title'] == 'Add Webclip':
            webclip(payload)
        if choice['title'] == 'Add Wifi':
            wifi(payload)
        if choice['title'] == 'Serve':
            cpload = profile.mkplist(payload)
            serve.run_server(cpload)
        if choice['title'] == 'Save':
            name = dialogs.input_alert('File name')
            name = name + '.mobileconfig'
            cpload = profile.mkplist(conf, pload)
            plistlib.writePlist(cpload, name)
    return payload

def main():
    c = None
    while c is None:
        c = setup()
    conf = profile.Config(**c)
    pload = profile.Payloads(conf)
    return [pload, conf]
    
pload, conf = main()
editpayload(pload)

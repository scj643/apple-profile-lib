# coding: utf-8
import plistlib
import uuid as u
from datetime import datetime
from io import BytesIO
import sys


try:
    import Crypto
    Crypto_support = True
except ImportError:
    Crypto_support = False
    print('No crypto support')

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

    def __init__(self, atrib, etype, atype=None):
        self.atrib = atrib
        self.etype = etype
        if atype:
            self.atype = type(atype)
        else:
            self.atype = 'unkown'

    def __str__(self):
        return 'Argument ' + repr(self.atrib) + ' is wrong type should be ' + repr(self.etype) + ' is ' + repr(
            self.atype)

def strip_dict(indict):
    """Strips keys with a value of None from a dict

    :param indict: Dictionary to be striped
    :return: Striped dictionary
    """
    out_dict = {k: v for k, v in indict.items() if v is not None}
    return out_dict


def uid():
    return u.uuid4().urn[9:].upper()


class Profile(object):
    """
    A Mobile Configuration Profile object
    """
    def __init__(self, identifier, uuid=uid(), description = None, display_name = None, organization = None,  expiration_date=None,
                 removal_date = None, duration_till_removal = None, scope = None, consent_text = None):
        """
        Note: Docstrings taken partly from
        https://developer.apple.com/library/content/featuredarticles/iPhoneConfigurationProfileRef/Introduction/Introduction.html
        :param identifier: A RDNS identifier (com.example.profile) Used to tell if a profile should be replaced or added
        :type identifier: str
        :param uuid: A unique identifier for the profile
        :type uuid: str
        :param description: Optional; A description shown in the detail screen for the profile Should be descriptive enough to let
        the user know if it should be installed
        :type description: str
        :param display_name: Optional; A human-readable name. displayed on the Detail screen. Doesn't have to be unique
        :type display_name: str
        :param organization: Optional; Human readable string that has the name of the organization that provided this profile
        :type organization: str
        :param expiration_date: Optional; A date when the profile is considered to have expired and can be updated OTA (Only used in OTA deliver)
        :type expiration_date: datetime
        :param removal_date: Optional; Date which the profile will be removed
        :type removal_date: datetime
        :param duration_till_removal: Optional; Number of seconds until the profile is auto removed
        :type duration_till_removal: float
        :param scope: Optional; Determines if payload should be installed for the system or user (used for keys typically)
                                valid options are user and system (MacOS only)
        :type scope: str
        :param consent_text: Optional; A dictionary containing consent or license agreemnet
                                       using the keys for each language region and a defualt key
                                       EX
                                       {'default', 'you agree to the terms provided with this profile'}
        :type consent_text: dict
        """
        self.PayloadDescription = description
        self.PayloadDisplayName = display_name
        self.PayloadExpirationDate = expiration_date
        self.PayloadIdentifier = identifier
        self.PayloadOrganization = organization
        self.PayloadUUID = uuid
        self.PayloadType = "Configuration"
        self.PayloadVersion = 1
        self.PayloadScope = scope
        self.RemovalDate = removal_date
        self.DurationUntilRemoval = duration_till_removal
        self.ConsentText = consent_text

    def strip(self):
        out_dict = {}
        for i in self.__dict__:
            if self.__dict__[i]:
                out_dict[i] = self.__dict__[i]
        return out_dict



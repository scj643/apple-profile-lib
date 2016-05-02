# iOS-Profile-Lib
## Description
This library allows you to create and verify iOS mobileconfig files right on your iOS device.  I could not find another iOS library for dealing with iOS mobileconfig files so I made this one.  It features type checking to prevent the creation of invalid mobileconfigs.

## Requirements
It will work with just the standard library for the most part.

To encrypt a profile __Crypto__ and __biplist__ are needed.

# ToDo
* [ ] implement some more config types
* [x] find out how to sign
* [ ] find out how to encrypt

I found out how to sign with OpenSSL but not how to encrypt.  See the docs at: https://developer.apple.com/library/ios/featuredarticles/iPhoneConfigurationProfileRef/Introduction/Introduction.html

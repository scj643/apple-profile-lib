# iOS-Profile-Lib
## Description
This library allows you to create and verify iOS mobileconfig files right on your iOS device.  I could not find another iOS library for dealing with iOS mobileconfig files so I made this one.  It features type checking to prevent the creation of invalid mobileconfigs.

## Requirements
It will work with just the standard library for the most part.
To encrypt a profile Crypto and biplist is needed.

#ToDo
Still need to implement some more config types and find out how to sign and encrypt
I found out how to sign with OpenSSL but not encrypt https://developer.apple.com/library/ios/featuredarticles/iPhoneConfigurationProfileRef/Introduction/Introduction.html is the documentation

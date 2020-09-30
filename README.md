# Apple Profile Lib
[![Build Status](https://travis-ci.org/scj643/iOS-Profile-Lib.svg?branch=master)](https://travis-ci.org/scj643/iOS-Profile-Lib)
## Description
This library allows you to create and verify mobileconfig files.
I could not find another library for dealing with mobileconfig files so I made this one.

It features type checking to prevent the creation of invalid mobileconfigs.

## Requirements
It will work with just the standard library for the most part.

To encrypt a profile __Crypto__ are needed.

# TODO
* [ ] implement some more config types
* [x] find out how to sign
* [ ] find out how to encrypt

I found out how to sign with OpenSSL but not how to encrypt.

See the docs at: https://developer.apple.com/library/ios/featuredarticles/iPhoneConfigurationProfileRef/Introduction/Introduction.html

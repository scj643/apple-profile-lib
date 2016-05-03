# Encrypt
I think this is how it might be done
```
openssl smime -encrypt -aes256 -outform pem -in payload.tmp -out payload-enc.tmp enckey.pem 
```
# Sign
```
openssl smime -sign -nodetach -in in.mobileconfig -signer signcert.crt -inkey signkey.pem -outform der -out signed.mobileconfig
```

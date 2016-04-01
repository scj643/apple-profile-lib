# coding: utf-8
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
import main as profile
import serve
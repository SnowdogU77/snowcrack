# genhash.py
#   NTLM hash generator
# By: Luke Jones

import hashlib
import binascii

def toHash():
    while True:
        pw = input("Password: ")
        print(str(binascii.hexlify(hashlib.new('md4', pw.encode('utf-16le')).digest()))[2:-1].upper()+"\n")
        
toHash()

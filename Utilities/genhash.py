# genhash.py
#   NTLM hash generator
# By: Luke Jones

import hashlib
import binascii

def toHash():
    while True:
        password = input("Password: ")
        hashtype = input("Encryption type: ")
        
        if hashtype == "ntlm":
            phash = hashlib.new('md4', password.encode('utf-16le')).digest()
            
        elif hashtype == "md4":
            phash = hashlib.new('md4', password.encode('ascii')).digest()

        elif hashtype == "md5":
            phash = hashlib.new('md5', password.encode("ascii")).digest()

        elif hashtype == "whirlpool":
            phash = hashlib.new('whirlpool', password.encode('ascii')).digest()
            
        elif hashtype == "sha1":
            phash = hashlib.sha1(password.encode('ascii')).digest()

        elif hashtype == "sha224":
            phash = hashlib.sha224(password.encode('ascii')).digest()

        elif hashtype == "sha256":
            phash = hashlib.sha256(password.encode('ascii')).digest()

        elif hashtype == "sha384":
            phash = hashlib.sha384(password.encode('ascii')).digest()

        elif hashtype == "sha512":
            phash = hashlib.sha512(password.encode('ascii')).digest()

        print("\n"+str(binascii.hexlify(phash))[2:-1]+"\n")
        
toHash()

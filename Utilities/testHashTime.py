import hashlib
import binascii
import time

def main():
    password = 'password'

    ntlmTimes = 0.0
    md4Times = 0.0
    md5Times = 0.0
    
    for i in range(100000):
        t = time.time()
        phash = hashlib.new('md4', password.encode('utf-16le')).digest()
        ntlmTimes += (time.time()-t)

        t = time.time()
        phash = hashlib.new('md4', password.encode('ascii')).digest()
        md4Times += (time.time()-t)
        
        t = time.time()
        phash = hashlib.md5(password.encode("ascii")).digest()
        md5Times += (time.time()-t)

    print("ntlm:", ntlmTimes/100000)
    print("md4:", md4Times/100000)
    print("md5:", md5Times/100000)
    
main()

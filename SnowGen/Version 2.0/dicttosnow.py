# dicttosnow.py
#   Converts dictionary text files to SnowCrack format
# By: Luke Jones

import os
import sys
import hashlib
import binascii
import time

#####
def toSnow(hashtype, infile=None, directory=sys.path[0]):
    """
    Generates a dictionary from UTF-8 dictionary file(s). Sourced from all
    files in working directory by default.
    ---
    outfile: Name given to dictionary, defaults to 'dictionary.sgn'.
    directory: Directory containing dictionaries, defaults to working directory.
    infile: Source from a single dictionary, not used by default.
    """
    
    print("Generating table...\n")
    out = []
    
    if infile != None:
        files = infile
    else:
        files = [f for f in os.listdir(directory)]
    
    for file in files:
        
        # Generate hash and append hash÷password to list
        try:
            dic = open(directory+file, 'r')
            
            for pw in dic:
                password = pw.rstrip()

                # Encrypt the password
                if hashtype == "ntlm":
                    phash = hashlib.new('md4', password.encode('utf-16le')).digest()
                    
                elif hashtype == "md4":
                    try:
                        phash = hashlib.new('md4', password.encode('ascii')).digest()
                    except UnicodeEncodeError:
                        phash = hashlib.new('md4', password.encode('utf-8')).digest()
                        
                elif hashtype == "md5":
                    try:
                        phash = hashlib.md5(password.encode("ascii")).digest()
                    except UnicodeEncodeError:
                        phash = hashlib.md5(password.encode('utf-8')).digest()
                        
                elif hashtype == "whirlpool":
                    try:
                        phash = hashlib.new('whirlpool', password.encode('ascii')).digest()
                    except UnicodeEncodeError:
                        phash = hashlib.new('whirlpool', password.encode('utf-8')).digest()
                        
                elif hashtype == "sha1":
                    try:
                        phash = hashlib.sha1(password.encode('ascii')).digest()
                    except UnicodeEncodeError:
                        phash = hashlib.sha1(password.encode('utf-8')).digest()
                        
                elif hashtype == "sha224":
                    try:
                        phash = hashlib.sha224(password.encode('ascii')).digest()
                    except UnicodeEncodeError:
                        phash = hashlib.sha224(password.encode('utf-8')).digest()
                        
                elif hashtype == "sha256":
                    try:
                        phash = hashlib.sha256(password.encode('ascii')).digest()
                    except UnicodeEncodeError:
                        phash = hashlib.sha256(password.encode('utf-8')).digest()
                        
                elif hashtype == "sha384":
                    try:
                        phash = hashlib.sha384(password.encode('ascii')).digest()
                    except UnicodeEncodeError:
                        phash = hashlib.sha384(password.encode('utf-8')).digest()
                        
                elif hashtype == "sha512":
                    try:
                        phash = hashlib.sha512(password.encode('ascii')).digest()
                    except UnicodeEncodeError:
                        phash = hashlib.sha512(password.encode('utf-8')).digest()
                        
                # If the hash isn't ntlm length, store as md5 to decrease file size
                # and limit runtime memory usage
                if not hashtype in ["ntlm", "md4", "md5"]:
                    phash = str(binascii.hexlify(phash))[2:-1]
                    phash = hashlib.md5(phash.encode("ascii")).digest()

                # Append the hash/password combination to the output list
                out.append(str(binascii.hexlify(phash))[2:-1] + "÷" + pw)
                    
            dic.close()

        # If the file isn't text or it hits a directory
        except (UnicodeDecodeError, PermissionError):
            print("Bad file")
        
    return out

#####
def sortDict(info, outfile='dictionary.sgn'):
    '''
    Removes duplicates and sorts file
    ---
    info: list of hashes and passwords separated by '÷'
    outfile: name of file to be outputted
    '''
    
    # Sketchy but fast duplicate removal
    lines = set(info)
    lines = [l.rstrip() for l in list(lines)]
    lines.sort()
    file = open(outfile, 'w')
    
    prev = []
    curh = ''
    curp = ''
    end = info[-1]
    
    for line in lines:
        try:
            h,p = line.split('÷')
            
            if curh == '':
                curh += h[:4]+'|'+h[4:]
                curp += p
                
            elif h[:4] == prev[0][:4]:
                curh += '|'+h[4:]
                curp += '¬'+p
                
            else:
                print(curh+'÷'+curp, file=file)
                curh, curp = '',''
                curh += h[:4]+'|'+h[4:]
                curp += p
                
            if h == end[0]:
                print(curh+'÷'+curp, file=file)
                
            prev = [h,p]
            
        except ValueError:
            pass
        
    file.close()

#####
def _toTime(raw):
    # Converts time to a useful format

    t = round(raw,2)
    if t < 60:
        return str(t)+" seconds"
    elif t < 3600:
        return str(t/60)+" minutes"
    else:
        return str(t/120)+ " hours"

#####
def main():
    hlist = ["ntlm","md4","md5","whirlpool","sha1","sha224","sha256","sha384","sha512"]
    
    indir = input("Input directory: ")
    outdir = input("Output directory: ")
    
    if indir == "":
        indir = sys.path[0]+"/"
    if outdir == "":
        outdir = sys.path[0]+"/"
    if not indir[-1] == "/" or "\\":
        indir += "/"
    if not outdir[-1] == "/" or "\\":
        outdir += "/"    
    
    while True:
        print("\nAvailible hash types:\n0-NTLM 1-MD4 2-MD5 3-Whirlpool 4-SHA1 5-SHA2(224) 6-SHA2(256) 7-SHA2(384) 8-SHA2(512)\n")

        ht = int(input("Hash type (number): "))
        try:
            if not ht in range(0,8):
                print("Invalid input!")
            else:
                hashtype = hlist[ht]
                break
        except ValueError:
            print("Invalid input!")
        
    x = time.time()
    inf = toSnow(hashtype, directory=indir)
    sortDict(inf,outfile=outdir+hashtype+' dict.sgn')
    print("Operation completed in {}".format(_toTime(time.time()-x)))

    
if __name__ == "__main__":
    main()

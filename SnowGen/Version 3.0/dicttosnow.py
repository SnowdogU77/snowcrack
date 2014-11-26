# dicttosnow.py
#   Converts dictionary text files to SnowCrack format
# By: Luke Jones

import os
import sys
import hashlib
import binascii
import time
from snowdict import SnowDict

#####
def toSnow(hashtype, filename, infile=None, directory=sys.path[0]):
    """
    Generates a dictionary from UTF-8 dictionary file(s). Sourced from all
    files in working directory by default.
    ---
    outfile: Name given to dictionary, defaults to 'dictionary.sgn'.
    directory: Directory containing dictionaries, defaults to working directory.
    infile: Source from a single dictionary, not used by default.
    """
    
    print("Generating table...\n")
    table = SnowDict(hashtype, fromdts=True)
    
    if infile != None:
        files = infile
    else:
        files = [f for f in os.listdir(directory)]
    
    for file in files:
        
        # Add password to table
        try:
            dic = open(directory+file, 'r')
            
            for pw in dic:
                password = pw.rstrip()

                # Encrypt the password
                table.addPassword(password)
                    
            dic.close()

        # If the file isn't text or it hits a directory
        except UnicodeDecodeError:
            print("Bad file")
        except PermissionError:
            pass
            
    table.sort()
    table.writeToFile(filename)
    
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
    fname = "{}{} dictionary.sgn".format(outdir,hashtype)
    toSnow(hashtype, fname, directory=indir)
    print("Operation completed in {}".format(_toTime(time.time()-x)))

    
if __name__ == "__main__":
    main()

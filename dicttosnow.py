# dicttosnow.py
#   Converts dictionary text files to SnowCrack format
# By: Luke Jones

import os
import sys
import hashlib
import binascii
import time


def toSnow(infile=None, directory=sys.path[0]):
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
        dic = open(directory+file, 'r')
        
        for passw in dic:
            pw = passw.rstrip()
            
            # Use hashlib library to encrypt the password with NTLM encryption
            phash = hashlib.new('md4', pw.encode('utf-16le')).digest()

            # Print the password to specfied file in this format: password   hash
            out.append(str(binascii.hexlify(phash))[2:-1].upper() + "÷" + pw)

        print(file, "added...")
        dic.close()
    
    return out


def noDupeSort(info, outfile = 'new dictionary.sgn'):
    # Removes duplicates and sorts file
    
    # Sketchy but fast duplicate removal
    lines = set(info)
    
    print("\nDuplicates removed...\nSorting...")
    lines = [l.rstrip() for l in list(lines)]
    lines.sort()
    
    print("Sorted...\nWriting file...")
    file = open(outfile, 'w')

    prev = ''
    curh = ''
    curp = ''
    
    for line in lines:
        try:
            h,p = line.split('÷')
            
            if curh == '':
                curh += h[:4]+'|'+h[4:]
                curp += p
                
            elif line[:4] == prev[:4]:
                curh += '|'+h[4:]
                curp += '¬'+p
                
            else:
                print(curh+'÷'+curp, file=file)
                curh, curp = '',''

            prev = line
            
        except ValueError:
            pass
        
    print('Done.\n')
    file.close()


def main():
    direct = input("Directory: ")
    x = time.time()
    if not direct[-1] == "/" or "\\":
        direct += "/"
    inf = toSnow(directory=direct)
    noDupeSort(inf)
    print(round(time.time()-x, 2))

    
if __name__ == "__main__":
    main()

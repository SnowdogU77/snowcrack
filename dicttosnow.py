# dicttosnow.py
#   Converts dictionary text files to SnowCrack format
# By: Luke Jones

import os
import sys
import hashlib
import binascii


def toSnow(outfile, infile=None, directory=sys.path[0]):
    """
    Generates a rainbow table from UTF-8 dictionary file(s). Sourced from all
    files in working directory by default.
    ---
    outfile: Name given to rainbow table, defaults to 'dictionary.sgn'.
    directory: Directory containing dictionaries, defaults to working directory.
    infile: Source from a single dictionary, not used by default.
    """
    
    print("Generating table...\n")
    out = open(outfile, 'w')
    
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
            print(str(binascii.hexlify(phash))[2:-1].upper() + "%" + pw, file=out)

        print(file, "added...")
        dic.close()
        
    out.close()

def noDupesSort(infile):
    # Removes duplicates and sorts file
    file = open(infile)
    
    # Sketchy but fast duplicate removal
    lines = set(file.readlines())
    print("\nDuplicates removed...\nSorting...")
    
    lines = [l.rstrip() for l in list(lines)]
    file.close()
    lines.sort()
    
    print("Sorted...\nWriting file...")
    file = open(infile, 'w')
        
    for line in lines:
        print(line, file=file)

    print('Done.\n')
    file.close()

def main():
    infile = input("Directory: ")
    toSnow(infile)
    noDupeSort(infile)

    
if __name__ == "__main__":
    main()

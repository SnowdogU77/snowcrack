# snowgen.py
#   A NTLM dictionary generator follwing the SnowCrack format
# By: Luke Jones

import getpass
import itertools
import time
import os
import hashlib
import binascii

   
######

def getchars(method):
    """Generates a charlist string either manually or via a wizard, and
    returns it along with minimum and maximum character restraints."""

    ### Character list:
    alpha = "abcdefghijklmnopqrstuvwxyz"
    upper = alpha.upper()
    numbers = "1234567890"
    challenge = "~`!@#$%^&*()_-+=[]{}|:;'<,>.?/ "
    ###
    
    charlist = ""
    name = ""

    # Charlist generation wizard
    if method == "w":
        print("\nReply y/n")

        if input("Lowercase letters? ")[0].lower() == "y":
            charlist += alpha
            name += "Alph"
  
        if input("Uppercase letters? ")[0].lower() == "y":
            charlist += upper
            name += "Caps"
            
        if input("Numbers? ")[0].lower() == "y":
            charlist += numbers
            name += "Nums"
            
        if input("Symbols? ")[0].lower() == "y":
            charlist += challenge
            name += "Chal"

    # Customized charlist
    if method == "c":
        name = input("Base file name: ")
        charlist = input("Insert characters:\n")
        
    while True:
        try:
            minlength = max(int(input("\nMinimum length? ")), 1)
            maxlength = max(int(input("Maximum length? ")), 2)
            break
        except ValueError:
            print("Incorrect input.")

    name += " {}-{}".format(minlength,maxlength)
    print("")
    
    return name, charlist, minlength, maxlength

######
def gentable(fname, charlist, minlength, maxlength):
    """Generates an NTLM rainbow table with a given charlist, and saves to a file."""
    file = open(fname+".sgn", 'w')
    x = time.time()
    count = 0
    
    # Iterates through possible lengths
    for passlen in range(minlength, maxlength):

        # Iterates through all possible passwords within length
        for char in itertools.product(charlist, repeat=passlen):

            # 7454000 lines creates a ~250MB file, also limits runtime
            # memory usage
            if (count%7454000 == 0 and count != 0):
                end = str(count//7454500)
                fn = file.name
                file.close()
                
                sorttable(fn)
                file = open(fname+" ~"+end, 'w')
                    
            password = ''.join(char)
            
            if password == "":
                break

            # Use hashlib library to encrypt the password with NTLM encryption
            phash = hashlib.new('md4', password.encode('utf-16le')).digest()

            # Print the password to specfied file in this format: hash%password
            # This format may be updated in the future to account for non-NTLM hashes
            # that include the % character
            print(str(binascii.hexlify(phash))[2:-1].upper() + "%" + password, file=file)
            count += 1
            
    file.close()
    
    if count < 7454000:
        sorttable(fname+".sgn")
        
    print("Runtime: {} with {} possible".format(time.time()-x, count))
    
######
def sorttable(infile):
    """Sorts rainbow tables using python's list sorting funtion"""
    
    file = open(infile)
    lines = [l.rstrip() for l in file.readlines()]
    file.close()
    print("Loaded into memory...")
    
    lines.sort()
    print("Sorted...\nWriting file...")

    file = open(infile, 'w')
        
    for line in lines:
        print(line, file=file)

    print('Done.\n')
    file.close()
    
######        
def main():
    print("SnowGen NTLM rainbow table generator.\n")

    try:
        while True:
            method = input("\nCharlist 'wizard' or 'custom?' ")[0].lower()

            if method != "w" and method != "c":
                print("Incorrect input.")
            else:
                break
        
        gentable(getchars(method))
        print("\nGeneration complete.\n")
        
    except (KeyboardInterrupt, EOFError):
        print("\nOperation canceled by user.\n")


if __name__ == "__main__":
    main()

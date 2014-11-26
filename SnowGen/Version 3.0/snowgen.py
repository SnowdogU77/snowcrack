# snowgen.py
#   A NTLM dictionary generator follwing the SnowCrack format
# By: Luke Jones

import itertools
import time
import hashlib
import binascii
from snowdict import SnowDict

   
######
def _getchars(method, directory):
    # Generates a charlist string either manually or via a wizard, and
    # returns it along with minimum and maximum character restraints.

    ### Character list:
    alpha = "abcdefghijklmnopqrstuvwxyz"
    upper = alpha.upper()
    numbers = "1234567890"
    challenge = "~`!@#$%^&*()_-+=[]{}|:;'<,>.?/ "
    ###
    
    hlist = ["ntlm", "md4", "md5", "whirlpool", "sha1", "sha224", "sha256", "sha384", "sha512"]
    charlist = ""
    name = directory
    
    # Charlist generation wizard
    while True:
        print("\nAvailible hash types:\n0-NTLM 1-MD4 2-MD5 3-Whirlpool 4-SHA1 5-SHA2(224) 6-SHA2(256) 7-SHA2(384) 8-SHA2(512)\n")

        try:
            ht = int(input("Hash type (number): "))
            if not ht in range(0,9):
                print("Invalid input!")
            else:
                hashtype = hlist[ht]
                name += hashtype + " "
                break
            
        except ValueError:
            print("Invalid input!")
    
    if method == "w":
        print("\nReply y/n")
        while True:
            try:
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
                break
            
            except IndexError:
                print("Incorrect input.\n")
                name = directory
                
    # Customized charlist
    if method == "c":
        name = input("Base file name: ")
        charlist = input("Insert characters:\n")
        
    while True:
        try:
            minlength = max(int(input("\nMinimum length? ")), 1)
            maxlength = max(int(input("Maximum length? ")), 1)+1
            break
        except ValueError:
            print("Incorrect input.")
            

    name += " {}-{}".format(minlength,maxlength-1)
    print("")
    
    return name, hashtype, charlist, minlength, maxlength

######
def gentable(fname, hashtype, charlist, minlength, maxlength, compress=False):
    """Generates an NTLM rainbow table with a given charlist, and saves to a file."""
    
    table = SnowDict(hashtype)
    x = time.time()
    sortlen = 7454000
    count = 0
    
    # Iterates through possible lengths
    for passlen in range(minlength, maxlength):

        # Iterates through all possible passwords within length
        for comb in itertools.product(charlist, repeat=passlen):

            # Limit to ~250MB per file, also limits runtime memory usage
            if (count%sortlen == 0 and count != 0):
                end = str(count//sortlen)
                fn = fname+" ~"+end+".psgn"
                table.sort()
                table.writeToFile(fn)
                table = SnowDict(hashtype)
            
            password = ''.join(comb)
            
            if password == "":
                break

            # Encrypt the password
            table.addPassword(password)
            count += 1
        
    if count < sortlen:
        table.sort()
        table.writeToFile(fname)
    
    print("Runtime: {} with {} possible".format(_toTime(time.time()-x), count))

#####
def _toTime(raw):
    # Converts time to a useful format

    t = round(raw,2)
    if t < 60:
        return str(t)+" seconds"
    elif t < 3600:
        return str(t/60)+" minutes"
    else:
        return str(t/120)+ "hours"

######        
def main():
    print("SnowGen NTLM rainbow table generator.\n")

    try:
        direct = input("Save directory: ")
        
        while True:
            method = input("\nCharlist 'wizard' or 'custom?' ")[0].lower()

            if method != "w" and method != "c":
                print("Incorrect input.")
            else:
                break

        compress = {'y':True, 'n':False}[input("""Use compression? This will take far longer, but the
                         files will be much smaller for longer hashtypes: """)[0].lower()]

        n,ht,ch,mi,ma = _getchars(method,direct)
        print("Generating table...\n")
        gentable(n,ht,ch,mi,ma,compress)
        print("\nGeneration complete.\n")
        
    except (KeyboardInterrupt, EOFError):
        print("\nOperation canceled by user.\n")

    
if __name__ == "__main__":
    main()

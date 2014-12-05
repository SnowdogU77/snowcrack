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
    challenge = "~`!@#$%^&*()_-+=[]{}|:;'<,>.?/\\ "
    ###
    
    hlist = ["ntlm", "md4", "md5", "whirlpool", "sha1", "sha224", "sha256", "sha384", "sha512"]
    charlist = ""
    fname = directory
    
    # Charlist generation wizard
    while True:
        print("\nAvailible hash types:\n0-NTLM 1-MD4 2-MD5 3-Whirlpool 4-SHA1 5-SHA2(224) 6-SHA2(256) 7-SHA2(384) 8-SHA2(512)\n")

        try:
            ht = int(input("Hash type (number): "))
            if not ht in range(0,9):
                print("Invalid input!")
            else:
                hashtype = hlist[ht]
                fname += hashtype + " "
                break
            
        except ValueError:
            print("Invalid input!")
    
    if method == "w":
        print("\nReply y/n")
        
        while True:
            try:
                if input("Lowercase letters? ")[0].lower() == "y":
                    charlist += alpha
                    fname += "Alph "
                    
                if input("Uppercase letters? ")[0].lower() == "y":
                    charlist += upper
                    fname += "Caps "
                    
                if input("Numbers? ")[0].lower() == "y":
                    charlist += numbers
                    fname += "Nums "
                    
                if input("Symbols? ")[0].lower() == "y":
                    charlist += challenge
                    fname += "Chal "
                break
            
            except IndexError:
                print("Incorrect input.\n")
                pass

    # Customized charlist       
    elif method == "c":
        fname = input("File name: ")
        charlist = input("Insert characters:\n")
        
    while True:
        try:
            minlength = max(int(input("\nMinimum length? ")), 1)
            maxlength = max(int(input("Maximum length? ")), 1)+1
            break
        except ValueError:
            print("Incorrect input.")
            

    fname += "{}-{}".format(minlength,maxlength-1)
    print("")

    compress = False
    
    if hashtype in ["whirlpool", "sha1", "sha224", "sha256", "sha384", "sha512"]:
        
        compress = input("\nUse compression? This will take far longer, but the files will be much smaller for longer hashtypes: ")[0].lower()
        if compress == "y":
            compress = True

    return fname, hashtype, charlist, minlength, maxlength, compress

######
def gentable(fname, hashtype, charlist, minlength, maxlength, useCompression):
    """Generates an NTLM rainbow table with a given charlist, and saves to a file."""
    
    table = SnowDict(hashtype, compress=useCompression)
    x = time.time()
    count = 0

    # Set the number of hashes to be stored per file. Limits to approximately 250MB files
    if (hashtype in ["whirlpool", "sha1", "sha224", "sha256", "sha384", "sha512"] and useCompression == False):
        sortlen = 1863500
    else:
        sortlen = 7454000
                    
    # Iterates through possible lengths
    for passlen in range(minlength, maxlength):

        # Iterates through all possible passwords within length
        for comb in itertools.product(charlist, repeat=passlen):

            # Handle file size / memory management
            if count%sortlen == 0 and count != 0:
                end = str(count//sortlen)
                if end == 1:
                    fn = fname+".sdct"
                else:
                    fn = fname+" ~"+end+".psdct"
                    
                table.sort()
                table.writeToFile(fn)
                table.clearTable()
            
            password = ''.join(comb)
            
            if password == "":
                break

            # Encrypt the password
            table.addPassword(password)
            count += 1
        
    if count < sortlen:
        table.sort()
        fname += ".sdct"
        table.writeToFile(fname)
    
    print("Runtime: {} with {} possible".format(_toTime(time.time()-x), count))

#####
def _toTime(raw):
    # Converts time to a useful format

    
    
    if raw < 60:
        return str(round(raw, 2))+" seconds"
    elif raw < 3600:
        return str(round(raw/60, 2))+" minutes"
    else:
        return str(round((raw/60)/60, 2))+ " hours"

######        
def main():
    print("SnowGen NTLM rainbow table generator.\n")

    try:
        direct = input("Save directory: ")

        if not direct[-1] in ["/","\\"]:
            direct += "/"
        
        while True:
            method = input("\nCharlist 'wizard' or 'custom?' ")[0].lower()

            if method != "w" and method != "c":
                print("Incorrect input.")
            else:
                break
            
        n,ht,ch,mi,ma,compress = _getchars(method,direct)
        
        print("\nGenerating table...\n")
        gentable(n,ht,ch,mi,ma,compress)
        print("\nGeneration complete.\n")
        
    except (KeyboardInterrupt, EOFError):
        print("\nOperation canceled by user.\n")

    
if __name__ == "__main__":
    main()

# snowgen.py
#   A NTLM dictionary generator follwing the SnowCrack format
# By: Luke Jones

import itertools
import time
import hashlib
import binascii

   
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
    
    charlist = ""
    name = directory

    # Charlist generation wizard
    
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
            maxlength = max(int(input("Maximum length? ")), 1)
            break
        except ValueError:
            print("Incorrect input.")

    name += " {}-{}".format(minlength,maxlength)
    print("")
    
    return name, charlist, minlength, maxlength+1

######
def gentable(fname, charlist, minlength, maxlength):
    """Generates an NTLM rainbow table with a given charlist, and saves to a file."""

    fn = fname+".sgn"
    x = time.time()
    count = 0
    out = []
    
    # Iterates through possible lengths
    for passlen in range(minlength, maxlength):

        # Iterates through all possible passwords within length
        for comb in itertools.product(charlist, repeat=passlen):

            # 7454000 lines creates a ~250MB file, also limits runtime
            # memory usage
            if (count%7454000 == 0 and count != 0):
                end = str(count//7454500)
                
                sorttable(out,fn)
                out = []
                fn = fname+" ~"+end+".psgn"
                    
            password = ''.join(comb)
            
            if password == "":
                break

            # Use hashlib library to encrypt the password with NTLM encryption
            phash = hashlib.new('md4', password.encode('utf-16le')).digest()

            # Append the hash/password combination to the output list
            out.append([str(binascii.hexlify(phash))[2:-1].upper(), password])
            count += 1
        
    if count < 7454000:
        sorttable(out, fn)
    
    print("Runtime: {} with {} possible".format(_toTime(time.time()-x), count))
    
######
def sorttable(info, fname):
    """Sorts rainbow tables using python's list sorting funtion"""

    info.sort()
    print("Sorted...\nWriting file...")

    file = open(fname, 'w')

    prev = []
    curh = ''
    curp = ''
    end = info[-1]
    
    for line in info:
        try:
            h,p = line
            
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

    print('Done.\n')
    file.close()

#####
def _toTime(raw):
    # Converts file input into proper format to stop case sensitivity

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

        n,ch,mi,ma = _getchars(method,direct)
        print("Beginning operation...\n")
        gentable(n,ch,mi,ma)
        print("\nGeneration complete.\n")
        
    except (KeyboardInterrupt, EOFError):
        print("\nOperation canceled by user.\n")

    
if __name__ == "__main__":
    main()

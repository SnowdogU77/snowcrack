# snowcrack.py
#   Binary search based dictionary cracking utility
# By: Luke Jones

from bisect import bisect_left
import os
import time

def crackMulti(inhash, file, directory):
    # Manages cracking using multi-part dictionaries which are tracked via the primary file name.

    print("\nSearching...")
    t = time.time()
    found = False
    
    for f in [f for f in next(os.walk(directory))[2] if f.startswith(file)]:
        table = open(directory+f, 'r')

        lines = table.readlines()
        leng = len(lines)-1

        pos = bisect_left(lines, inhash)
        
        try:
            line = lines[pos]
            spl = line.index("%")
            has,pas = line[:spl], line[spl+1:]

            if not (pos == 0 or not inhash == has):
                print("Success! Password is:", pas)
                print("Runtime: {} seconds".format(round(time.time()-t, 2)))
                
                table.close()
                found = True
                break
        
        except IndexError:
            pass

        table.close()

    if not found:
        print("Password not found.\n")
        
    input("\nPress enter to exit...")
    print("")


def crackSingle(inhash,file):
    # Manages single-file cracking operations
    
    print("\nSearching...")
    t = time.time()
    table = open(file, 'r')
    lines = table.readlines()
    table.close()
    
    pos = bisect_left(lines, inhash)

    try:
        line = lines[pos]
        spl = line.index("%")
        has,pas = line[:spl], line[spl+1:]
        
    except IndexError:
        print("Password not found!\n")
        return
        
    if (pos == 0 or not inhash == has):
        print("Password not found!\n")
    else:
        print("Success! Password is:", pas)
        print("Runtime: {} seconds".format(round(time.time()-t, 2)))

    input("Press enter to exit...")
    print("")
    
def main():
    # Dictionary file is given by user. Script runs through dictionary using
    # a binary search to locate hash, retreives password.
    
    while True:
        inhash = input("Hash: ")
        if len(inhash) == 32:
            break
        else:
            print("Invalid hash!\n")
            
    file = input("Dictionary file: ")

    if file.count("/") > 0 or file.count("\\") > 0:
        di = file.rfind("/")
        
        if di == -1:
            di = file.rfind("\\")
                
        directory = file[:di+1]
        fname = file[di+1:-4]
            
    else:
        directory = sys.path[0]
        fname = file
    
    for f in next(os.walk(directory))[2]:
        if os.path.isfile(file.split(".")[0]+" ~1"):
            crackMulti(inhash, fname, directory)
            return
        
    crackSingle(inhash, fname, directory)
        

main()

# snowcrack.py
#   Binary search based dictionary cracking utility
# By: Luke Jones

from bisect import bisect_left
import os
import time
import sys

######
def crackMulti(inhash, file, directory):
    """crackMulti manages cracking using multi-part dictionaries which are tracked
    via the base file name.
    -
    inhash: hash to crack
    file: base dictionary file (.sgn)"""

    print("\nSearching...")
    t = time.time()
    found = False

    files = [file] + [directory+f for f in next(os.walk(directory))[2] if f.startswith(file[:-4]+" ~")]
    
    for f in files:
        table = open(f, 'r')

        lines = table.readlines()
        heads = [l[:4] for l in lines]
        
        head = inhash[:4]
        tail = inhash[4:]
        pos = bisect_left(heads, head)
        
        try:
            line = lines[pos]
            hashes,passes = line.split("÷")
            hashes = hashes.split("|")[1:]
            passes = passes.split("¬")
            m = hashes.index(tail)
            pas = passes[m]

            if not pos == 0:
                print("\nSuccess! Password is:", pas)
                print("Runtime: {}".format(_toTime(time.time()-t)))
                
                table.close()
                found = True
                break
        
        except ValueError:
            pass

        table.close()

    if not found:
        print("Password not found.\n")
        
    input("\nPress enter to exit...")
    print("")

######
def crackSingle(inhash,file):
    """crackSingle manages cracking using a single file.
    -
    inhash: hash to crack
    file: dictionary file (.sgn)"""
        
    print("\nSearching...")
    t = time.time()
    table = open(file, 'r')
    lines = table.readlines()
    heads = [l[:4] for l in lines]
    
    table.close()

    head = inhash[:4]
    tail = inhash[4:]
    pos = bisect_left(heads, head)

    try:
        line = lines[pos]
        hashes,passes = line.split("÷")
        hashes = hashes.split("|")[1:]
        passes = passes.split("¬")
        m = hashes.index(tail)
        pas = passes[m]
        
    except ValueError:
        return
        
    print("Success! Password is:", pas)
    print("Runtime: {}".format(_toTime(time.time()-t)))

######
def _toTime(raw):
    # Converts time in seconds to appropriate format
    
    t = round(raw,2)
    
    if t < 60:
        return str(t)+" seconds"
    elif t < 3600:
        return str(t/60)+" minutes"
    else:
        return str(t/120)+ "hours"

######
def _digestFile(file):
    # Converts file input into proper format to stop case sensitivity

    di = None

    if file.count("\\") != 0:
        di = file.rfind("\\")+1
    elif file.count("/") != 0:
        di = file.rfind("/")+1
    else:
        directory = sys.argv[0]

    if di != None:
        directory = file[:di]
        
    fname = file[di+1:-4]
    end = file[-4:]
    rfname = ""

    if "alph" in fname:
        rfname += "Alph"
    if "caps" in fname:
        rfname += "Caps"
    if "nums" in fname:
        rfname += "Nums"
    if "chal" in fname:
        rfname += "Chal"
    if rfname != "":
        rfname += " "+fname[len(rfname)+1:]+end
        fname = rfname
        
    return fname, directory

######  
def main():
    # Dictionary file is given by user. Script runs through dictionary using
    # a binary search to locate hash, retreives password.

    print("SnowCrack dictionary cracker.\n\n")
    
    while True:
        inhash = input("Hash: ")
        if len(inhash) == 32:
            break
        else:
            print("Invalid hash!\n")

    while True:
        file = input("Dictionary file: ")

        if os.path.isfile(file):
            break
        else:
            print("Dictionary not found!\n")

    fname, directory = _digestFile(file)
    
    for f in next(os.walk(directory))[2]:
        if f.startswith(fname.split(".")[0]+" ~"):
            crackMulti(inhash, fname, directory)
            return
        
    crackSingle(inhash, file)

    input("\nPress enter to exit...")
    print("")


if __name__ == "__main__":
    main()

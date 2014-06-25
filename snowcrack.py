# snowcrack.py
#   Binary search based dictionary cracking utility
# By: Luke Jones

from bisect import bisect_left

def main():
    # Dictionary file is given by user. Script runs through dictionary using
    # a binary search to locate hash, retreives password.
    
    while True:
        inhash = input("Hash: ")
        if len(inhash) == 32:
            break
        else:
            print("Invalid hash!\n")
            
    file = input("Dictionary file (blank defaults to dictionary.sgn): ")

    if file == "":
        file = "dictionary.sgn"
        
    print("\nSearching...")
    
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

    input("Press enter to exit...")
    print("")


main()

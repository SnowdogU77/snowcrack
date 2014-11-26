import hashlib
import binascii

class SnowDict():
    def __init__(self, hashtype, fromdts=False):
        """A SnowDict is a dictionary of passwords and hashes for use
        with the SnowCrack suite."""
        
        self._data = []
        self._hashtype = hashtype
        self._isSorted = False
        self._fromdts = fromdts
        
    #####
    def _digestFileName(self, filename):
    # Converts file input into proper format to stop case sensitivity

        di = None

        if filename.count("\\") != 0:
            di = filename.rfind("\\")+1
        elif filename.count("/") != 0:
            di = filename.rfind("/")+1
        else:
            directory = sys.path[0]+"\\"

        if di != None:
            directory = filename[:di]
            
        fname = filename[di:-4]
        end = ".sgn"
        rfname = ""
        norm = False
        
        if ("alph" in fname or "Alph" in fname):
            rfname += "Alph"
        if ("caps" in fname or "Caps" in fname):
            rfname += "Caps"
        if ("nums" in fname or "Nums" in fname):
            rfname += "Nums"
        if ("chal" in fname or "Chal" in fname):
            rfname += "Chal"
        if rfname != "":
            rfname += " "+fname[len(rfname)+1:]+end
            fname = rfname
        else:
            fname += end
            
        return directory+fname

    ####
    def _isFromDict(self):
        if "fromdts" in self._data[0]:
            return True
        else:
            return False
        
    #####
    def sort(self):
        """Sort sorts the dictionary into proper SnowCrack format.
        Once sorted, additions cannot be made to it, nor can it
        be re-sorted."""
        
        if len(self._data) == 0:
            raise ValueError("Dictionary is empty")

        if not self._isSorted:
            # Sketchy but fast duplicate removal
            if self._isFromDict():
                lines = set(self._data)
                lines = [l.rstrip() for l in list(lines)]
            else:
                lines = self._data
            lines.sort()

            data = []
            prev = []
            curh = ''
            curp = ''
            end = lines[-1]
            
            for line in lines:
                try:
                    h,p = line.split('÷')
                    
                    if curh == '':
                        curh += h[:4]+'|'+h[4:]
                        curp += p
                        
                    elif h[:4] == prev[0][:4]:
                        curh += '|'+h[4:]
                        curp += '¬'+p
                        
                    else:
                        data.append(curh+'÷'+curp)
                        curh, curp = '',''
                        curh += h[:4]+'|'+h[4:]
                        curp += p
                        
                    if line == end:
                        data.append(curh+'÷'+curp)
                        
                    prev = [h,p]
                    
                except ValueError:
                    pass
                
            self._data = data
            self._isSorted = True

        else:
            raise ValueError("Dictionary is already sorted")
        
    ####
    def addPassword(self, password):
        hashtype = self._hashtype
        
        if not self._isSorted:
            if hashtype == "ntlm":
                phash = hashlib.new('md4', password.encode('utf-16le')).digest()
                
            elif hashtype == "md4":
                try:
                    phash = hashlib.new('md4', password.encode('ascii')).digest()
                except UnicodeEncodeError:
                    phash = hashlib.new('md4', password.encode('utf-8')).digest()
                    
            elif hashtype == "md5":
                try:
                    phash = hashlib.md5(password.encode("ascii")).digest()
                except UnicodeEncodeError:
                    phash = hashlib.md5(password.encode('utf-8')).digest()
                    
            elif hashtype == "whirlpool":
                try:
                    phash = hashlib.new('whirlpool', password.encode('ascii')).digest()
                except UnicodeEncodeError:
                    phash = hashlib.new('whirlpool', password.encode('utf-8')).digest()
                    
            elif hashtype == "sha1":
                try:
                    phash = hashlib.sha1(password.encode('ascii')).digest()
                except UnicodeEncodeError:
                    phash = hashlib.sha1(password.encode('utf-8')).digest()
                    
            elif hashtype == "sha224":
                try:
                    phash = hashlib.sha224(password.encode('ascii')).digest()
                except UnicodeEncodeError:
                    phash = hashlib.sha224(password.encode('utf-8')).digest()
                    
            elif hashtype == "sha256":
                try:
                    phash = hashlib.sha256(password.encode('ascii')).digest()
                except UnicodeEncodeError:
                    phash = hashlib.sha256(password.encode('utf-8')).digest()
                    
            elif hashtype == "sha384":
                try:
                    phash = hashlib.sha384(password.encode('ascii')).digest()
                except UnicodeEncodeError:
                    phash = hashlib.sha384(password.encode('utf-8')).digest()
                    
            elif hashtype == "sha512":
                try:
                    phash = hashlib.sha512(password.encode('ascii')).digest()
                except UnicodeEncodeError:
                    phash = hashlib.sha512(password.encode('utf-8')).digest()
                    
            # If the hash isn't ntlm length, store as md5 to decrease file size
            # and limit runtime memory usage
            if not hashtype in ["ntlm", "md4", "md5"]:
                phash = str(binascii.hexlify(phash))[2:-1]
                phash = hashlib.md5(phash.encode("ascii")).digest()

            # Append the hash/password combination to self._data
            self._data.append(str(binascii.hexlify(phash))[2:-1] + "÷" + password)

        else:
            raise ValueError("Dictionary is already sorted")

    ####
    def writeToFile(self, filename):
        if self._sorted:
            fname = self._digestFileName(filename)
            file = open(fname, 'w')
            if fromdts:
                print("fromdts", file=file)
            for item in self._data:
                print(item, file=file)
            file.close()
        else:
            raise ValueError("Cannot write unsorted table")
            

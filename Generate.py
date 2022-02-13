import hashlib

from datetime import datetime
import time

from numpy import byte

class pe_generator() :
    
    def __init__(self,entrypoint, imagebase,SectionAlignment,FileAlignment) :
        self.binary = bytearray()
        
        self.entrypoint = entrypoint.to_bytes(4,'little')
        self.imagebase = imagebase.to_bytes(4,'little')
        self.sectionalignment = SectionAlignment.to_bytes(4,'little')
        self.filealignment = FileAlignment.to_bytes(4,'little')
    
    def run(self) :
        self._generate_dos_header()
        self._generate_nt_header()
        self.generate()
    
    def generate(self) :
        sha256 = hashlib.sha256(self.binary).hexdigest()
        file_path = 'generated/'
        file = file_path+sha256+'.exe'
        with open(file,'wb') as f :
            f.write(self.binary)
    
    def _generate_dos_header(self) :
        dos_header = bytearray(b'MZ')
        dos_header_padding = bytearray([0]*58)
        dos_header = dos_header+dos_header_padding
        nt_header_offset = bytearray([64,0,0,0])
        dos_header = dos_header + nt_header_offset

        self.binary = dos_header
    
    def _generate_nt_header(self):
        nt_header = bytearray()
        
        # IMAGE_FILE_HEADER
        signature = bytearray(b'PE')+bytearray([0]*2)   #Signature
        machine = bytearray(int('8664', 16).to_bytes(2,byteorder='little')) #Machiene : X64
        nt_header = signature+machine
        numberofsection = (4).to_bytes(2,'little')
        nt_header +=numberofsection
        timedatestamp = int(time.mktime(datetime.today().timetuple())).to_bytes(4,'little')
        nt_header +=timedatestamp
        nt_header += bytearray([0]*8)
        size_of_optionalheader = bytearray([224,0])
        nt_header +=size_of_optionalheader
        characteristic = bytearray([2,1])
        nt_header += characteristic
        
        #IMAGE_OPTIONAL_HEADER
        magic = bytearray([11,2])
        nt_header += magic
        nt_header += bytearray([0]*14)
        
        nt_header += self.entrypoint
        base_of_code = self.filealignment
        base_of_data = self.filealignment
        nt_header += (base_of_code+base_of_data)
        nt_header += self.imagebase
        nt_header += self.sectionalignment
        nt_header += self.filealignment
        
        size_of_header = self.filealignment*4
        
        self.binary += nt_header

    def _generate_section_header(self) :
        pass





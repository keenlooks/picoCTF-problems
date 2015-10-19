import os
from hacksport.problem import Remote, ProtectedFile
import string

class Problem(Remote):
    program_name = "broken_rsa.py"
    files = [ProtectedFile("flag")]

    def initialize(self):
        # generate random 32 hexadecimal characters
        self.enc_key = ''.join(self.random.choice(string.digits + 'abcdef') for _ in range(32))
        #self.welcome_message = "Welcome to Secure Encryption Service version 1.{}".format(self.random.randint(0,10))

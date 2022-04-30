import traceback
from cryptography.fernet import Fernet

def gen_key():
    return Fernet.generate_key()

def load(filepath, *keypath):
    # tries to load key from file, alternatively uses the argument self as key
    try:
        keypath = keypath[0]
        if keypath:
            try:
                with open(keypath, 'rb') as keyfile:
                    key = keyfile.read()
            except FileNotFoundError:
                print("Couldn't find keyfile, quitting.")
        else:
            key = gen_key()
    except IndexError:   # if no key is given, a new one is generated
        key = gen_key()

    # loads file from filename in the flags dict
    try:
        with open(filepath, 'rb') as file:
            fileData = file.read()
    except FileNotFoundError:
        print("Couldn't find provided file.\nQuitting!")
        quit()

    return fileData, key
# loads required key and file

def encrypt(filedata, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(filedata)
    return encrypted

def decrypt(filedata, key):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(filedata)
    return decrypted.decode()
# decrypts the given binary data with provided key

def save(savefile, data, *key):
    try:
        try:
            with open(savefile + ".lol", 'wb') as file:
                file.write(data)
            with open(savefile + '.key', 'wb') as file:
                file.write(key[0])
        except Exception:
            traceback.print_exc()
            return 1
        return 0
    except Exception:
        traceback.print_exc()



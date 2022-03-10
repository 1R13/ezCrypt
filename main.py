'''This is just a small module to simplify encryption and decryption in further projects.'''
import traceback

from cryptography.fernet import Fernet
from sys import argv


def gen_key():
    return Fernet.generate_key()

def get_flags():
    flags = {'-k': None, '-f': None, '-m': None, '-o': None, '-v': False}
    for f in flags:
        try:
            if argv[argv.index(f) + 1] != "-k" and argv[argv.index(f) + 1] != "-f":
                flags[f] = argv[argv.index(f) + 1]
            else:
                pass
        except ValueError:
            pass
        except IndexError:
            pass
    return flags
# requires all arguments from the commandline

def load(flags):
    # tries to load key from file, alternatively uses the argument self as key
    if flags["-k"]:
        try:
            with open(flags["-k"], 'rb') as keyfile:
                key = keyfile.read()
        except FileNotFoundError:
            print("Couldn't find keyfile, quitting.")
            quit()
    else:   # if no key is given, a new one is generated
        key = gen_key()

    # loads file from filename in the flags dict
    try:
        with open(flags["-f"], 'rb') as file:
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
    print(type(filedata))
    fernet = Fernet(key)
    decrypted = fernet.decrypt(filedata)
    return decrypted.decode()
# decrypts the given binary data with provided key

def save(flags, data, *key):
    if flags["-o"]:
        savefile = flags["-o"]
    else:
        savefile = flags["-f"]
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


def main():

    flags = get_flags()
    if flags["-f"] == None or flags["-m"] == None:
        print("No enough arguments given!")
        quit()
    filedata, key = load(flags)

    if flags["-v"]:
        print("Using Key : %s" % key.decode())

    if flags["-m"] == "encrypt":
        result = encrypt(filedata, key)
        save(flags, result, key)

    elif flags["-m"] == "decrypt":
        if flags["-k"]:
            result = decrypt(filedata, key)
        else:
            print("Missing Key!")
            quit()

    print(key)
    print(result)



if __name__ == '__main__':
    main()
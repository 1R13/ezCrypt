from ezCrypt_src import EzCrypt
from sys import argv


def help():
    print("Usage :\npython3 %s <options>\n\nOptions:\n-f\t\t\tfile path\n-m <decrypt|encrypt>\tmodus operandi\n"
        "-k <path_to_key>\tkey_file path\n-v\t\t\tverbose Output\n-o <output_file>\toutput file in decrypt mode" % argv[0])


def get_flags():
    if argv.__contains__("-h") or argv.__contains__("--help"):
        help()
        quit()

    flags = {'-k': None, '-f': None, '-m': None, '-o': None, '-v': False}
    for f in flags:
        if flags[f] == False:
            flags[f] = bool(flags[f] - 1)
        try:
            if argv[argv.index(f) + 1] != "-k" and argv[argv.index(f) + 1] != "-f":
                flags[f] = argv[argv.index(f) + 1]
            elif type(flags[f]) == bool:
                flags[f] == bool(flags[f] - 1)

        except ValueError:
            pass
        except IndexError:
            pass
    return flags
# requires all arguments from the commandline

def main():

    flags = get_flags()
    if flags["-f"] == None or flags["-m"] == None:
        print("Not enough arguments given!")
        help()
        quit()
    file_data, key = EzCrypt.load(flags["-f"], flags["-k"])

    if flags["-v"]:
        print("Using Key : %s" % key.decode())

    if flags["-m"] == "encrypt":
        result = EzCrypt.encrypt(file_data, key)
        if flags["-o"]:
            EzCrypt.save(flags["-o"], result, key)
        else:
            EzCrypt.save(flags["-f"], result, key)

    elif flags["-m"] == "decrypt":
        if flags["-k"]:
            result = EzCrypt.decrypt(file_data, key)
        else:
            print("Missing Key!")
            quit()
    if flags["-v"]:
        print(key)
        print(result)



if __name__ == '__main__':
    main()
import os
import hashlib
import csv

duplicates = []


def remove_duplicates():
    try:
        os.remove('duplicate.csv')
    except FileNotFoundError:
        pass


def write_duplicate(x, path, directory):
    file = f"{x}|    {path}"
    with open('duplicate.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([directory])
        writer.writerow([file])
        writer.writerow([f"HASH: {hash_file(path, '', hash_algo)}"])
        writer.writerow([])


def remove_manifest():
    try:
        os.remove('manifest.csv')
    except FileNotFoundError:
        pass


def create_manifest(x, path):
    file = f"{x}|    {path}"
    with open('manifest.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([file])


def compute_directory(directory, rename, hash_algo):
    x = 0
    y = 0
    try:
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)

            if os.path.isfile(path):
                hash_value = hash_file(path, filename, hash_algo)
                if hash_value not in duplicates:
                    try:
                        if rename:
                            duplicates.append(hash_value)
                            rename_file(path, hash_value)
                        y = y + 1
                        create_manifest(y, path)
                    except Exception as e:
                        raise Exception(f"\nCritical error in file: {path}\nError: {str(e)}")
                else:
                    x += 1
                    write_duplicate(x, path, directory)

            elif os.path.isdir(path):
                compute_directory(path, rename, hash_algo)

    except Exception as e:
        raise Exception(f"\nCritical error in directory: {directory}\nError: {str(e)}")



def get_extension(file_name):
    split = os.path.splitext(file_name)
    return split[1]


def hash_file(file_src, old_name, hash_algo):
    extension = get_extension(old_name)

    hasher = hash_algo
    with open(file_src, 'rb') as file_found:
        while chunk := file_found.read(8192):
            hasher.update(chunk)

    new_name = hasher.hexdigest() + extension
    new_file_path = os.path.join(os.path.dirname(file_src), new_name)
    return new_file_path


def rename_file(old_name, new_name):
    if not os.path.exists(new_name):
        os.rename(old_name, new_name)


def print_menu():
    choice = int(input("Enter your choice:\n"
                       "0: End program\n"
                       "1: Hash and rename files starting from directory (all subdirectory included) "
                       "Manifest file auto included.\n"
                       "2: Only create manifest file\n"
                       "3: Delete manifest file\n"
                       "4: Delete duplicates list file\n"
                       )
                 )

    return choice



def get_hash_algo(number):

    if number == 1:
        hash_algo = hashlib.md5()
        print("Hashing files using: MD-5")
        print("\nWarning: md5 may have collisions in the hashed name and cause errors resulting to false "
              "duplicates...\n\n")
    elif number == 2:
        hash_algo = hashlib.sha1()
        print("Hashing files using: sha-1")
        print("\nWarning: sha-1 may have collisions in the hashed name and cause errors resulting to false "
              "duplicates...\n\n")
    elif number == 3:
        print("Hashing files using: sha-224")
        hash_algo = hashlib.sha224()
    elif number == 4:
        print("Hashing files using: sha-256")
        hash_algo = hashlib.sha256()
    elif number == 5:
        print("Hashing files using: sha-384")
        hash_algo = hashlib.sha384()
    elif number == 6:
        print("Hashing files using: sha-512")
        hash_algo = hashlib.sha512()
    elif number == 7:
        print("Hashing files using: sha3-224")
        hash_algo = hashlib.sha3_224()
    elif number == 8:
        print("Hashing files using: sha3-384")
        hash_algo = hashlib.sha3_384()
    elif number == 9:
        print("Hashing files using: sha512-512")
        hash_algo = hashlib.sha3_512()
    elif number == 10:
        print("Hashing files using: shake-128")
        hash_algo = hashlib.shake_128()
    elif number == 11:
        print("Hashing files using: shake-256")
        hash_algo = hashlib.shake_256()
    else:
        print("CRITICAL ERROR: Critical error occurred when determining hash algorithm")
    return hash_algo

def get_hashtype():
    number = 0

    while number < 1 or number > 11:
        number = int(input("Choose the hash algorithm you want to use:\n"
                           "1: MD-5\n"
                           "2: sha-1\n"
                           "3: sha-224\n"
                           "4: sha-256\n"
                           "5: sha-384\n"
                           "6: sha-512\n"
                           "7: sha3-224\n"
                           "8: sha3-384\n"
                           "9: sha3-512\n"
                           "10: shake-128\n"
                           "11: shake-256\n"
                           )
                     )
        if number < 1 or number > 11:
            print("Invalid choice. Please try again.")
    return get_hash_algo(number)



if __name__ == '__main__':

    try:
        param = print_menu()

        if param == 1:
            hash_algo = get_hashtype()
            name = input("Enter the directory you want to rename to hash value [USE C NOTATION] \n"
                         "Manifest file automatically created"
                         "(Example C:/Users/name/Desktop):\n")
            remove_manifest()
            remove_manifest()

            compute_directory(name, True, hash_algo)
            print("\nFiles renamed and manifest file created\n")

        elif param == 2:
            hash_algo = hashlib.sha256()
            name = input("Enter the directory you want to create a manifest file for [USE C NOTATION] "
                         "(Example C:/Users/name/Desktop):\n")
            remove_manifest()
            compute_directory(name, False, hash_algo)
            print("\nManifest file successfully created\n")

        elif param == 3:
            remove_manifest()
            print("Manifest file removed")

        elif param == 4:
            remove_duplicates()
            print("Duplicates file removed")

        else:
            print("Invalid Choice")

    except:
        print("Invalid Choice\nYou must choose a valid item from the menu")


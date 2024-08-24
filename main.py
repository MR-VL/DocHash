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
        writer.writerow([f"HASH: {hash_file(path, '')}"])
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


def compute_directory(directory, rename):
    x = 0
    y = 0
    try:
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)

            if os.path.isfile(path):
                hash_value = hash_file(path, filename)
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
                compute_directory(path, rename)

    except Exception as e:
        raise Exception(f"\nCritical error in directory: {directory}\nError: {str(e)}")


def compute_file(src):
    file_name = os.path.basename(src)
    new_name = hash_file(src, file_name)
    rename_file(src, new_name)


def get_extension(file_name):
    split = os.path.splitext(file_name)
    return split[1]


def hash_file(file_src, old_name):
    extension = get_extension(old_name)

    hasher = hashlib.sha256()
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


if __name__ == '__main__':
    param = -1

    while param != 0:
        try:
            param = print_menu()

            if param == 0:
                break

            elif param == 1:
                name = input("Enter the directory you want to rename to hash value [USE C NOTATION] \n"
                             "Manifest file automatically created"
                             "(Example C:/Users/name/Desktop):\n")
                remove_manifest()
                remove_manifest()
                compute_directory(name, True)
                print("\nFiles renamed and manifest file created\n")

            elif param == 2:
                name = input("Enter the directory you want to create a manifest file for [USE C NOTATION] "
                             "(Example C:/Users/name/Desktop):\n")
                remove_manifest()
                compute_directory(name, False)
                print("\nManifest file successfully created\n")

            elif param == 3:
                remove_manifest()
                print("Manifest file removed")

            elif param == 4:
                remove_duplicates()
                print("Duplicates file removed")

            else:
                print("Invalid Choice")
                param = print_menu()

        except:
            print("Invalid Choice\nYou must choose a valid item from the menu")
            param = print_menu()

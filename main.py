import os
import hashlib
import csv

duplicates = []


def remove_duplicates():
    try:
        os.remove('duplicate.csv')
    finally:
        return


def write_duplicate(x, path, directory):
    file = str(x) + "|    " + path
    with open('duplicate.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([directory])
        writer.writerow([file])
        writer.writerow(["HASH: " + hash_file(path, "")])
        writer.writerow([])


def compute_directory(directory):
    x = 0
    try:
        for filename in os.listdir(directory):

            path = os.path.join(directory, filename)

            if os.path.isfile(path) and duplicates.append(path):
                try:
                    compute_file(path)
                except Exception as e:
                    raise Exception(f"\n Critical error in file: {path}\nError: {str(e)} ")
            else:
                x = x + 1
                write_duplicate(x, path, directory)
    except Exception as e:
        raise Exception(f"\n Critical error in directory: {directory} \nError: {str(e)}")


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

    new_name = hasher.hexdigest()
    new_name = new_name + extension

    new_file_path = os.path.join(os.path.dirname(file_src), new_name)
    return new_file_path


def rename_file(old_name, new_name):
    os.rename(old_name, new_name)


if __name__ == '__main__':
    remove_duplicates()
    name = input("Enter the directory you want to rename to hash value [USE C NOTATION] "
                 "(Example C:/Users/name/Desktop):\n")
    compute_directory(name)

# C:\Users\miket\Downloads\test
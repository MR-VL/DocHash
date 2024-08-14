import os
import hashlib


def compute_directory(directory):
    compute_file(directory)


def compute_file(src):
    file_name = os.path.basename(src)
    hash_file(src, file_name)

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
    rename_file(file_src, new_file_path)


def rename_file(old_name, new_name):
    os.rename(old_name, new_name)


if __name__ == '__main__':

    name = input("Enter the directory you want to rename to hash value [USE C NOTATION] "
                 "(Example C:/Users/name/Desktop):\n")
    compute_directory(name)


#C:\Users\miket\Downloads\test.pdf
#Hash
# text.pdf
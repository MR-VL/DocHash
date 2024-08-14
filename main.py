import os
import hashlib

def compute_directory(directory):
    compute_file(directory)


def compute_file(file_name):
    file_name = os.path.basename(file_name)
    print(file_name)
    hash_file(file_name)

def hash_file(directory):
    hasher = hashlib.sha256(directory.encode('utf-8'))
    print(hasher.hexdigest())

if __name__ == '__main__':

    name = input("Enter the directory you want to rename to hash value [USE C NOTATION] (Example C:/Users/name/Desktop):\n")
    compute_directory(name)


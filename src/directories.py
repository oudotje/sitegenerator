import os
import shutil

def copy_content(source, dest):
    if os.listdir(dest) != []:
        for file in os.listdir(dest):
            filepath = os.path.join(dest, file)
            print(f"cleaning destination {filepath}") 
            if os.path.isdir(filepath):
                shutil.rmtree(filepath)
            elif os.path.isfile(filepath):
                os.remove(filepath)

    files = os.listdir(source)
    for file in files:
        filepath = os.path.join(source, file)
        if os.path.isfile(filepath):
            print(f"copying: {filepath} in {dest}")
            shutil.copy(filepath, dest)
        elif os.path.isdir(filepath):
            dest_path = os.path.join(dest, file)
            print(f"creating directory: {dest_path}")
            os.mkdir(dest_path)
            print(f"copying directory: {filepath} in {dest_path}")
            copy_content(filepath, dest_path)

import directories
from textnode import *

def main():
    source = "/home/jean/workspace/github.com/oudotje/sitegenerator/static"
    dest = "/home/jean/workspace/github.com/oudotje/sitegenerator/public"
    directories.copy_content(source, dest)

if __name__ == "__main__":
    main()

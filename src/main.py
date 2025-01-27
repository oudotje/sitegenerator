import directories
import markdown
from textnode import *

def main():
    source = "/home/jean/workspace/github.com/oudotje/sitegenerator/static"
    dest = "/home/jean/workspace/github.com/oudotje/sitegenerator/public"
    template_path = "/home/jean/workspace/github.com/oudotje/sitegenerator/template.html"
    md_source = "/home/jean/workspace/github.com/oudotje/sitegenerator/content/"
    directories.copy_content(source, dest)
    markdown.generate_pages_recursive(md_source, template_path, dest)

if __name__ == "__main__":
    main()

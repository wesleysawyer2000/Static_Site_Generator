from textnode import *
from htmlnode import *
from directories import *
import sys


def main():

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # Copy and overwrite from one directory to another
    if os.path.exists("docs"):
        shutil.rmtree("docs") # Delete content in destination directory

    # Generate Page
    copy_to("static", "docs", basepath)
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
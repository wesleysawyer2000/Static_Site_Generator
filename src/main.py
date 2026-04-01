from textnode import *
from htmlnode import *
from directories import *


def main():

    # Copy and overwrite from one directory to another
    if os.path.exists("public"):
        shutil.rmtree("public") # Delete content in destination directory
    copy_to("static", "public")

    # Generate Page
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
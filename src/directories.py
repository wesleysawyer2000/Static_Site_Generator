import os
import shutil
import re
from pathlib import Path
from conversions import *


# recursive function that copies all the contents from a source directory to a destination directory
def copy_to(directory_source, directory_destination):
    # Check if Source Exists
    if os.path.exists(directory_source) is False:
        raise Exception("ERROR: Source directory does NOT exist")
    files_source = os.listdir(directory_source)  # list of directories/files in source directory
    # Check if destination
    if os.path.exists(directory_destination) is False:
        os.mkdir(directory_destination)
    # Copy Files
    for file_source in files_source:
        file_source_full = os.path.join(directory_source, file_source) # Get full path to file location
        if os.path.isfile(file_source_full) is True:
            shutil.copy(file_source_full, directory_destination)
        else:
            directory_destination_new = os.path.join(directory_destination, file_source)
            copy_to(file_source_full, directory_destination_new)


def extract_title(markdown):
    pattern = r"^\s*#(?!\s*#)\s*(.*?)\s*$"
    matches = re.findall(pattern, markdown, re.MULTILINE)
    if not matches:
        raise Exception("ERROR: No header in markdown")
    return matches[0].strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Convert Markdown to file and extract the title + content
    file_from = open(from_path, "r")
    markdown = file_from.read()
    html_content = markdown_to_html_node(markdown)
    html_content_new = html_content.to_html()
    html_title = extract_title(markdown)
    file_from.close()
    # Plug in title and content values into template
    file_template = open(template_path, "r+")
    html_template = file_template.read()
    html_template_clean1 = html_template.replace("{{ Title }}", html_title)
    html_template_clean2 = html_template_clean1.replace("{{ Content }}", f"{html_content_new}")
    file_template.close()
    # Copy to new destination
    dest_directory = os.path.dirname(dest_path)
    if os.path.exists(dest_directory) is False:
        os.makedirs(dest_directory, exist_ok=True)
    file_dest = open(dest_path, "w")
    file_dest.write(html_template_clean2)
    file_dest.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


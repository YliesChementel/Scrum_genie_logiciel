import os
import subprocess
import argparse
import xml.etree.ElementTree as ET

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='PDF to Text/XML Parser')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-t', '--text', action='store_true', help='Generate text output')
group.add_argument('-x', '--xml', action='store_true', help='Generate XML output')
args = parser.parse_args()

print("Script started")

# Chemin vers le dossier contenant les PDF
SOURCE_DIR = "."
DEST_DIR = "Processed"

# Create the destination directory if it doesn't exist
if not os.path.exists(DEST_DIR):
    print(f"Creating {DEST_DIR}")
    os.makedirs(DEST_DIR)
else:
    print(f"{DEST_DIR} already exists")

def extract_info_from_text(file_text):
    # Initialize extracted information
    title = "Unknown"
    authors = "Unknown"
    abstract = "Unknown"
    references = "Unknown"

    # Attempt to extract information
    lines = file_text.splitlines()
    if lines:
        title = lines[0]

    # Similar logic can be used to extract authors, abstract, and references
    # ... (Implement extraction logic here)

    return title, authors, abstract, references

def create_xml_output(info, subdir_path, subdir_name):
    title, authors, abstract, references = info

    # Create XML structure
    root = ET.Element("article")
    ET.SubElement(root, "preamble").text = subdir_name
    ET.SubElement(root, "title").text = title
    ET.SubElement(root, "author").text = authors
    ET.SubElement(root, "abstract").text = abstract
    ET.SubElement(root, "biblio").text = references

    # Write XML to file
    tree = ET.ElementTree(root)
    xml_path = os.path.join(subdir_path, f"{subdir_name}.xml")
    tree.write(xml_path)

# Processing loop
for filename in os.listdir(SOURCE_DIR):
    print(f"Checking file: {filename}")
    if filename.endswith(".pdf"):
        print(f"Processing file: {filename}")
        file_path = os.path.join(SOURCE_DIR, filename)

        # Create a subdirectory for each PDF
        subdir_name = filename.replace(".pdf", "")
        subdir_path = os.path.join(DEST_DIR, subdir_name)
        if not os.path.exists(subdir_path):
            print(f"Creating directory: {subdir_path}")
            os.makedirs(subdir_path)
        else:
            print(f"Directory {subdir_path} already exists")

        # Copy the PDF to the subdirectory
        dest_pdf_path = os.path.join(subdir_path, filename)
        os.system(f"cp '{file_path}' '{dest_pdf_path}'")

        # Convert the PDF to text
        print(f"Converting PDF: {filename}")
        dest_txt_path = os.path.join(subdir_path, f"{subdir_name}_pdftotext.txt")
        subprocess.run(["pdftotext", file_path, dest_txt_path])

        # Read the content of the text file
        with open(dest_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Extract necessary information
        print(f"Extracting info from: {filename}")
        extracted_info = extract_info_from_text(content)

        # Create output based on selected format
        if args.xml:
            create_xml_output(extracted_info, subdir_path, subdir_name)
        elif args.text:
            # Create a text file with extracted elements
            info_path = os.path.join(subdir_path, f"{subdir_name}_info.txt")
            with open(info_path, 'w') as f:
                title, authors, abstract, _ = extracted_info
                f.write(f"File: {filename.replace(' ', '_')}\n")
                f.write(f"Title: {title}\n")
                f.write(f"Authors: {authors}\n")
                f.write(f"Abstract: {abstract}\n")

print("Script finished")

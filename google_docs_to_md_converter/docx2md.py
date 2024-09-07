import subprocess
import re
import sys

def convert_docx_to_md(docx_file, pandoc_md_file):
    """Converts a .docx file to Markdown using pandoc."""
    try:
        print(f"Converting {docx_file} to {pandoc_md_file} using pandoc...")
        subprocess.run(
            ["pandoc", "--extract-media=.", "-i", docx_file, "-o", pandoc_md_file],
            check=True
        )
        print("Pandoc conversion successful.")
    except subprocess.CalledProcessError:
        print("Error: Pandoc conversion failed.")
        sys.exit(1)

def extract_pandoc_image_references(pandoc_md_file):
    """Extracts image references from the Pandoc-generated Markdown file."""
    image_references = []
    # Adjust regex to handle multi-line image references
    image_pattern = re.compile(r'!\[.*?\]\(./media/(image[0-9]+\.png)\)\{.*?\}', re.DOTALL)

    print(f"Extracting image references from {pandoc_md_file}...")
    with open(pandoc_md_file, 'r') as pandoc_file:
        content = pandoc_file.read()  # Read the entire file content
        matches = image_pattern.findall(content)
        for match in re.finditer(image_pattern, content):
            image_reference = match.group(0)
            print(f"Found image: {image_reference}")
            image_references.append(image_reference)

    print(f"Total images extracted: {len(image_references)}")
    return image_references

def replace_gdoc_images(gdoc_file, output_file, image_references):
    """Replaces base64 images in the Google Docs-exported Markdown file with Pandoc images."""
    base64_pattern = re.compile(r'!\[\]\[image[0-9]+\]')
    image_index = 0
    replaced_images = 0

    print(f"Replacing base64 images in {gdoc_file} with extracted images...")

    with open(gdoc_file, 'r') as gdoc, open(output_file, 'w') as output:
        for line in gdoc:
            # Check if the line contains a base64 image reference
            if base64_pattern.search(line):
                if image_index < len(image_references):
                    print(f"Replacing base64 image at line: {line.strip()}")
                    print(f"With: {image_references[image_index]}")
                    output.write(image_references[image_index] + '\n')
                    image_index += 1
                    replaced_images += 1
                else:
                    print(f"No matching Pandoc image for line: {line.strip()}")
                    output.write(line)
            else:
                output.write(line)

    print(f"Replaced {replaced_images} images in total.")

def clean_base64_references(output_file):
    """Removes base64 image definitions from the end of the Markdown file."""
    base64_definition_pattern = re.compile(r'<data:image/png;base64,.*')

    print("Cleaning base64 image definitions from the file...")

    with open(output_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            if not base64_definition_pattern.search(line):
                file.write(line)

    print("Base64 image definitions removed.")

def main():
    if len(sys.argv) != 3:
        print("Usage: gdoc2md <input_file.docx> <gdoc_export.md>")
        sys.exit(1)

    docx_file = sys.argv[1]
    gdoc_file = sys.argv[2]

    # Output file for Pandoc Markdown
    pandoc_md_file = f"{docx_file.rsplit('.', 1)[0]}_pandoc.md"
    
    # Output file for the final result
    output_file = f"{gdoc_file.rsplit('.', 1)[0]}_imported.md"

    # Step 1: Convert the .docx file to Markdown using pandoc
    convert_docx_to_md(docx_file, pandoc_md_file)

    # Step 2: Extract image references from the Pandoc Markdown file
    image_references = extract_pandoc_image_references(pandoc_md_file)

    # Step 3: Replace base64 images in the Google Docs Markdown file with the extracted Pandoc images
    replace_gdoc_images(gdoc_file, output_file, image_references)

    # Step 4: Remove base64 image definitions at the end of the output file
    clean_base64_references(output_file)

    print(f"Conversion completed. Output saved to {output_file}")

if __name__ == "__main__":
    main()
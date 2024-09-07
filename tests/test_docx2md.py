import unittest
import os
from google_docs_to_md_converter.docx2md import convert_docx_to_md, extract_pandoc_image_references, replace_gdoc_images, clean_base64_references

class TestDocxToMdConverter(unittest.TestCase):

    def setUp(self):
        self.docx_file = 'tests/mocks/document.docx'  # Replace with your actual mock docx file path
        self.gdoc_file = 'tests/mocks/document.md'  # Your Google Docs exported markdown file
        self.pandoc_md_file = 'tests/mocks/sample_pandoc.md'  # Output file for pandoc conversion
        self.output_file = 'tests/mocks/document_imported.md'  # Final output file

    def test_convert_docx_to_md(self):
        print(f"Converting {self.docx_file} to {self.pandoc_md_file} using pandoc...")
        convert_docx_to_md(self.docx_file, self.pandoc_md_file)
        self.assertTrue(os.path.exists(self.pandoc_md_file))

    def test_extract_pandoc_image_references(self):
        convert_docx_to_md(self.docx_file, self.pandoc_md_file)
        image_references = extract_pandoc_image_references(self.pandoc_md_file)
        self.assertIsInstance(image_references, list)
        self.assertTrue(len(image_references) > 0, "Expected at least one image reference, but found none.")

    def test_replace_gdoc_images(self):
        convert_docx_to_md(self.docx_file, self.pandoc_md_file)
        image_references = extract_pandoc_image_references(self.pandoc_md_file)
        replace_gdoc_images(self.gdoc_file, self.output_file, image_references)
        self.assertTrue(os.path.exists(self.output_file))
        

    def test_clean_base64_references(self):
         # Ensure the output file exists before cleaning
        if not os.path.exists(self.output_file):
            convert_docx_to_md(self.docx_file, self.pandoc_md_file)
            image_references = extract_pandoc_image_references(self.pandoc_md_file)
            replace_gdoc_images(self.gdoc_file, self.output_file, image_references)

        clean_base64_references(self.output_file)
        with open(self.output_file, 'r') as file:
            content = file.read()
            self.assertNotIn('<data:image/png;base64,', content)

    def tearDown(self):
        # Clean up the generated files after tests
        for file in [self.pandoc_md_file, self.output_file]:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main()

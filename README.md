# Google Docs to Markdown Converter

## Context

In modern documentation workflows, especially with collaborative tools like Google Docs, it is often necessary to export documents in different formats, such as `.docx` (Word) and `.md` (Markdown). Unfortunately, both the Pandoc export of `.docx` to `.md` and the Google Docs Markdown export present limitations:
 
- **Pandoc Export**: While it provide the best image quality the Markdown structure it produce from a `.docx` can be complex or incomplete.
- **Google Docs Markdown Export**: Google Docs natively supports exporting a document as Markdown (`File > Download > Markdown`), but the images are low-resolution and embedded in base64 format, making the output difficult to manage.

By combining the two approaches, we aim to create a Markdown file that is easy to work with and contains high-quality images. 

This script uses a heuristic approach to merge the advantages of both exports. Due to the limitations of both export methods, some compromises had to be made based on some heuristic:

- The heuristic depends on the order of the images in the two files being the same. If the images are not in the same order, the script might not match them correctly.
- Complex Markdown elements like tables or very custom layouts may require some manual adjustments after running the script.

### The Solution implemented

This project proposes a Python script (`docx2md.py`) that combines the strengths of both exports:

- **High-quality images** are extracted from the Pandoc export.
- **The markdown structure** is extracted from the Google Docs Markdown export.
- **final markdown** : is created replacing the low-resolution base64 images in the Google Docs Markdown export with the high-quality images from the Pandoc export.

By doing so, we leverage the strengths of both tools to achieve a good-quality Markdown file with well-formatted content and clear images.


## Usage

### Export `.docx` from Google Docs
1. Open your Google Doc.
2. Go to the menu `File > Download > Microsoft Word (.docx)`.
3. Save the `.docx` file to your local machine.

### Export Markdown from Google Docs
1. Google Docs natively supports exporting to Markdown as well.
2. Go to the menu `File > Download > Markdown (.md)`.
3. Save the Markdown file to your local machine.

### Run the command

Once you have exported both the `.docx` file and the Markdown file from Google Docs, you can use the `docx2md.py` script to combine them into a final, well-formatted Markdown file with high-quality images.
Steps:

1. Place the `.docx` file and `.md` file from Google Docs in the same directory as the script or any working directory of your choice.
2. Run the script from the command line:

```bash
gdoc2md tests/mocks/document.docx tests/mocks/document.md
```

There results will be saved in the current working directory:

- `document_imported.md` the final markdown file with high-quality images.
- `media/` all the images extracted.


The script will:
1. Convert the `.docx` file to Markdown using Pandoc.
2. Extract the images from the Pandoc export.
3. Replace the low-quality base64-encoded images in the Google Docs Markdown export with the high-resolution images from the Pandoc export.
4. Save the final output to a new Markdown file named `your_exported_gdoc_imported.md`.


## Install the tool with pipx

Prerequisites: 

- `pandoc`

To Install Pandoc:

```bash
# Ubuntu
sudo apt update
sudo apt install pandoc

# macOS (with Homebrew)
brew install pandoc
```

Install the tool locally:
```bash
cd into this repo
pipx install .
```

To reinstall use ``--force`:

```
pipx install --force .
```


Reopen a terminal and the tool will be globally available as `gdoc2md`.

## Development

To run the tool in development use `poetry run python3 google_docs_to_md_converter/docx2md.py` instead of `gdoc2md`

### Install Python Dependencies

This tools uses poetry:

```
poetry install
poetry shell
```

### Run tests

Run all tests:
```bash
PYTHONPATH=. poetry run pytest tests
```

Run a single test function in a file:
```bash
PYTHONPATH=. poetry run pytest tests/test_docx2md.py::TestDocxToMdConverter::test_convert_docx_to_md
```

Where:
* `PYTHONPATH=.` is used to tell pytest to use the current directory as the Python path.
* `poetry run` is used to tell pytest to use the Python interpreter managed by Poetry.
* `TestDocxToMdConverter` is the test class.
* `test_convert_docx_to_md` is the test function to run of the `TestDocxToMdConverter` class.

#### Mock Google Doc

To run the tests, you need to have a Google Doc ID. You can use the following command to download the Google Doc and save it as a mock document. The exported mock are expoported in tests/mocks/ but you can change the DOC_ID to download other documents or modify the document and download it again and commit the changes.

```bash
poetry run python3 tests/download_and_mock.py
```


## Other Problems with exported content that this tool doesn't address

### When Google Code Block Add-On is used the result markdown is a table not a code block

In the process of exporting code snippets from Google Docs to Markdown, users often encounter formatting issues. The Code Block Google Doc add-on, while useful, can produce exports that are not well-structured in Markdown. This can result in single-line outputs, strange characters, and code being placed within tables, making it difficult to read and use effectively. 

#### Semi automatic Solution for a single code block
This can be easily fixed with the right prompt.

```markdown
# Context
The code block that I will provide you:
- was formatted with [Code Block Google doc add-on](https://workspace.google.com/u/1/marketplace/app/code\_blocks/100740430168):
- than it has been exported from google doc to markdown
- the resulting export is not well formatted in markdown: it is single line, it contains some strange chars, it is contained in table.

# Objective
I'll wiil paste below the exported markdown, please clean it up, detect the programming language and configure the markdown to use the right code highlight. Output only the code block in markdown, avoid explanations.

# The exported markdown
<MARKDOWN_CODE_BLOCK HERE>
```

#### Semi Solution For the whole document

If your Google Doc contains multiple code blocks, and you want to fix them all, you can adapt the prompt to handle an entire document with several code blocks. The following prompt should be used to automatically identify and clean all code blocks in the document:

```markdown
# Context
The markdown document that I will provide you:
- was exported from Google Docs where code blocks were formatted using [Code Block Google Doc add-on](https://workspace.google.com/u/1/marketplace/app/code_blocks/100740430168):
- then it was exported from Google Docs to Markdown.
- the resulting export contains multiple code blocks that are not well formatted: they are in single lines, contain strange characters, and are enclosed within tables.

# Objective
Please go through the entire markdown document, detect all the code blocks, clean them up, detect the programming language for each code block, and configure the markdown to use the appropriate code highlighting. Output only the cleaned-up code blocks in markdown with the correct code highlighting.

# The exported markdown document
<WHOLE_MARKDOWN_DOCUMENT_HERE>
```

import requests
import os

def download_doc(doc_id, file_format='docx'):
    url = f"https://docs.google.com/document/d/{doc_id}/export?format={file_format}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    dir_path = 'tests/mocks/'
    os.makedirs(dir_path, exist_ok=True)  # Create directory if it doesn't exist
    file_path = f'{dir_path}document.{file_format}'  # Save with format in filename
    with open(file_path, 'wb') as f:
        f.write(response.content)

def main(doc_id):
    download_doc(doc_id, 'docx')  # Download in docx format
    download_doc(doc_id, 'md')     # Download in md format

if __name__ == "__main__":
    DOC_ID = "131T0cvLKR_CJ_h7hdIy3o9ft0pkx3eEOtO3jeErxgsg"
    main(DOC_ID)

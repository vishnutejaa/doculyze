# PDF to CSV Table Extractor Documentation

## Overview

This Python application extracts tabular data from PDF files by converting them into images, processing the images using the OpenAI API to extract structured data, and then saving the results as CSV files. The process involves three main steps:

1. Converting a PDF file into a series of PNG images.
2. Using OpenAI's GPT-4o model to extract tabular data from the images.
3. Converting the extracted data into CSV format.

The application is modular, with separate functions for each step, and includes error handling to ensure robustness.

## Requirements

- **Python 3.7+**
- **Libraries**:
  - `os` (built-in), json` (built-in), `base64` (built-in)
  - `pdf2image` (`pip install pdf2image`)
  - `pandas` (`pip install pandas`)
  - `openai` (`pip install openai`)
  - `Pillow` (`pip install Pillow`)
- **External Dependency**:
  - Poppler: Required by `pdf2image` for PDF-to-image conversion. Install it separately:
    - Windows: Download and add to PATH (e.g., via `conda install -c conda-forge poppler`)
    - Linux/macOS: `sudo apt-get install poppler-utils` or `brew install poppler`


- **OpenAI API Key**: Replace `"your-api-key"` in the code with a valid OpenAI API key.



## Usage

1. **Set Up**:
   - Install the required libraries using `pip`.
   - Ensure Poppler is installed and accessible in your system PATH.
   - Replace `"your-api-key"` with your OpenAI API key.
   - Update the `pdf_path` variable in the `main()` function with the path to your PDF file.

2. **Run the Script**:
   ```bash
   python script_name.py
   ```
   The script will:
   - Convert the PDF to images (saved in `extracted_images/`).
   - Process the images with OpenAI to extract tables (saved in `extracted_txt_files/` as text files).
   - Convert the extracted text to CSV files (saved in `extracted_csv_files/`).

3. **Output**:
   - Images: PNG files named `page_1.png`, `page_2.png`, etc., in `extracted_images/`.
   - Text Files: Extracted data as `response1.txt`, `response2.txt`, etc., in `extracted_txt_files/`.
   - CSV Files: Structured data as `response1.csv`, `response2.csv`, etc., in `extracted_csv_files/`.

## Functions

### `convert_pdf_to_images(pdf_path, output_folder="extracted_images", dpi=500)`

**Description**: Converts a PDF file into a series of PNG images.

**Parameters**:
- `pdf_path` (str): Path to the input PDF file.
- `output_folder` (str, optional): Directory to save the extracted images. Defaults to `"extracted_images"`.
- `dpi` (int, optional): Dots per inch for image resolution. Higher values increase detail but require more processing. Defaults to `500`.

**Behavior**:
- Converts each PDF page to an image using `pdf2image`.
- Creates the output folder if it doesn’t exist.
- Saves images as `page_1.png`, `page_2.png`, etc.
- Prints progress messages.
- Raises `ValueError` if no images are extracted.

**Example**:
```python
convert_pdf_to_images("example.pdf", dpi=300)
```

---

### `encode_image(image_path)`

**Description**: Encodes an image file into a base64 string for use with the OpenAI API.

**Parameters**:
- `image_path` (str): Path to the image file.

**Returns**:
- `str`: Base64-encoded string of the image, or `None` if encoding fails.

**Behavior**:
- Reads the image in binary mode.
- Encodes it to base64 and decodes to UTF-8.
- Prints an error message and returns `None` if encoding fails.

**Example**:
```python
encoded = encode_image("extracted_images/page_1.png")
```

---

### `process_images_with_openai(image_folder="extracted_images", output_folder="extracted_txt_files")`

**Description**: Processes images using the OpenAI API to extract tabular data and saves the results as text files.

**Parameters**:
- `image_folder` (str, optional): Directory containing the input images. Defaults to `"extracted_images"`.
- `output_folder` (str, optional): Directory to save the extracted text files. Defaults to `"extracted_txt_files"`.

**Behavior**:
- Creates the output folder if it doesn’t exist.
- Processes only `.png` files, sorted alphabetically.
- Encodes each image to base64.
- Sends the image to OpenAI’s GPT-4o model with instructions to extract tabular data.
- Saves the response as `response1.txt`, `response2.txt`, etc.
- Handles errors gracefully with printed messages.

**Example**:
```python
process_images_with_openai()
```

---

### `convert_text_to_csv(input_folder="extracted_txt_files", output_folder="extracted_csv_files")`

**Description**: Converts extracted text files (assumed to contain JSON data) into CSV files.

**Parameters**:
- `input_folder` (str, optional): Directory containing the text files. Defaults to `"extracted_txt_files"`.
- `output_folder` (str, optional): Directory to save the CSV files. Defaults to `"extracted_csv_files"`.

**Behavior**:
- Creates the output folder if it doesn’t exist.
- Reads each `.txt` file, removes JSON markdown (```json```), and parses it as JSON.
- Converts the JSON data into a pandas DataFrame.
- Saves the DataFrame as a CSV file (e.g., `response1.csv`).
- Prints success or error messages.

**Example**:
```python
convert_text_to_csv()
```

---

### `main()`

**Description**: Orchestrates the entire workflow.

**Behavior**:
- Defines the PDF file path (must be updated by the user).
- Calls `convert_pdf_to_images()`, `process_images_with_openai()`, and `convert_text_to_csv()` in sequence.

**Example**:
```python
main()
```

---

## Notes

- **API Key Security**: Store the OpenAI API key securely (e.g., in an environment variable) rather than hardcoding it.
- **Error Handling**: The script includes basic error handling, but you may want to add more robust logging for production use.
- **Performance**: High DPI settings or large PDFs may increase processing time and memory usage.
- **OpenAI Costs**: Processing multiple images may incur API usage costs.

## Example Workflow

1. Input: `example.pdf` (a 2-page PDF with tables).
2. Run the script:
   - Images saved: `extracted_images/page_1.png`, `extracted_images/page_2.png`.
   - Text files saved: `extracted_txt_files/response1.txt`, `extracted_txt_files/response2.txt`.
   - CSV files saved: `extracted_csv_files/response1.csv`, `extracted_csv_files/response2.csv`.

---


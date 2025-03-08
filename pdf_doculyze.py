import os
import json
import base64
import pdf2image
import pandas as pd
import openai
from PIL import Image

# OpenAI API Key - if you have an OpenAI account, you can set your API key here
# You can also set the API key as an environment variable named OPENAI_API_KEY
# import os
# openai.api_key = os.getenv("OPENAI_API_KEY")

## (or) you can set the API key directly here (usually not recommended for security reasons) and the general syntax of the key is as follows: sk-87997d8d-7b3d-4b3d-8b3d-8b3d8b3d8b3d
# openai.api_key = "sk-your-actual-key-here"



# Sequential conversion of pdf to images
def convert_pdf_to_images(pdf_path, output_folder="extracted_images", dpi=500): #dpi is dots per inch; indicates the clarity and detail of an image; higher dpi means more detail and more processing required
    """Converts a PDF into images and saves them as PNG files."""
    print("\n--- PDF PROCESSING ---")
    
    # PDF to a list of images conversion
    pdf_images = pdf2image.convert_from_path(pdf_path, dpi=dpi)

    if not pdf_images:
        raise ValueError("No images extracted from the PDF!")

    # Create output directory
    os.makedirs(output_folder, exist_ok=True)

    # Save each page as an image
    for i, image in enumerate(pdf_images):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        image.save(image_path)
        print(f"Saved page {i+1} as {image_path}")

def encode_image(image_path):
    """Encodes an image file as a base64 string."""
    try:
        with open(image_path, "rb") as img:
            return base64.b64encode(img.read()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding {image_path}: {e}")
        return None

def process_images_with_openai(image_folder="extracted_images", output_folder="extracted_txt_files"):
    """Processes images in a folder using OpenAI API and extracts text."""
    os.makedirs(output_folder, exist_ok=True)

    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(".png")])

    for idx, image_file in enumerate(image_files, start=1):
        image_path = os.path.join(image_folder, image_file)
        print(f"Processing {image_file}...")

        base64_image = encode_image(image_path)
        if not base64_image:
            continue

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Extract tabular data from this image and return it in a structured format."},
                    {"role": "user", "content": [
                        {"type": "text", "text": "Extract tables from this image and return structured data."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]}
                ],
                max_tokens=2000,
            )
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
            continue

        extracted_text = response.choices[0].message.content if response.choices else ""

        # Save extracted text
        output_filename = os.path.join(output_folder, f"response{idx}.txt")
        try:
            with open(output_filename, 'w', encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"Saved extracted data to {output_filename}")
        except Exception as e:
            print(f"Error saving {output_filename}: {e}")


def convert_text_to_csv(input_folder="extracted_txt_files", output_folder="extracted_csv_files"):
    """Reads extracted text files, parses JSON content, and saves them as CSV files."""
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                raw_content = file.read()

            # Clean and parse JSON content
            cleaned_content = raw_content.strip("```json").strip("```")

            try:
                data = json.loads(cleaned_content)
                df = pd.DataFrame(data)

                # Save as CSV
                csv_file_path = os.path.join(output_folder, filename.replace(".txt", ".csv"))
                df.to_csv(csv_file_path, index=False)
                print(f"Saved CSV file: {csv_file_path}")

            except json.JSONDecodeError as e:
                print(f"Error processing {filename}: {e}")

def main():
    pdf_path = "path/to/pdf_file.pdf"  

    convert_pdf_to_images(pdf_path)

    process_images_with_openai()

    convert_text_to_csv()

if __name__ == "__main__":
    main()

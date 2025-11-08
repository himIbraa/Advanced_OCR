import os
from pathlib import Path
from pdf2image import convert_from_path
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Function to process PDF and extract images
def process_pdf_extract_images(file_path):
    logging.info(f"Received file: {file_path}")

    media_root = Path("./media")
    media_root.mkdir(parents=True, exist_ok=True)
    pdf_folder = media_root / file_path.stem
    pdf_folder.mkdir(parents=True, exist_ok=True)

    try:
        # Convert PDF to images
        logging.info("Processing PDF file")
        dpi = 200
        fmt = 'png'

        images = convert_from_path(
            file_path,
            dpi=dpi
        )

        if not images:
            raise FileNotFoundError("No images were created from the PDF.")

        for i, image in enumerate(images):
            image_path = pdf_folder / f"page_{i + 1}.png"
            image.save(image_path, fmt.upper())
            logging.info(f"Saved image: {image_path}")

        logging.info("All pages extracted successfully.")

        return True

    except Exception as e:
        logging.error(f"Error occurred during PDF image extraction: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    # Replace Name PDF with your pdf
    file_path = Path("./PDF/file_1603715661690.pdf")
    if not file_path.exists():
        logging.error(f"Error: The file {file_path} does not exist.")
    else:
        success = process_pdf_extract_images(file_path)

        if success:
            logging.info("PDF processed successfully.")
        else:
            logging.error("Failed to process PDF.")

import os
import io
import re
import json
import time
import logging
from google.cloud import vision

# ------------------------------------------------------------
# BASIC CONFIGURATION
# ------------------------------------------------------------
logging.basicConfig(level=logging.INFO)

# credentials.json must be in the same folder as your notebook
credentials_path = os.path.join(os.getcwd(), "credentials.json")
if not os.path.exists(credentials_path):
    raise FileNotFoundError("❌ credentials.json not found in current folder")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Initialize Vision API client
try:
    client = vision.ImageAnnotatorClient()
    logging.info("✅ Google Vision API client initialized")
except Exception as e:
    logging.exception("❌ Failed to initialize Vision client")
    raise e

# ------------------------------------------------------------
# IMAGE FOLDER CONFIGURATION
# ------------------------------------------------------------
folders_path = "./media/info"

if not os.path.exists(folders_path):
    raise FileNotFoundError(f"❌ Folder not found: {folders_path}")

images = [img for img in os.listdir(folders_path)
          if img.lower().endswith((".png", ".jpg", ".jpeg"))]

if not images:
    raise ValueError(f"❌ No image files found in {folders_path}")

# Sort pages logically (page_1.png, page_2.png, etc.)
images.sort(key=lambda x: int(re.search(r'page_(\d+)', x).group(1))
            if re.search(r'page_(\d+)', x) else float('inf'))

# ------------------------------------------------------------
# OCR PROCESSING LOOP
# ------------------------------------------------------------
ocr_results = {}
logging.info(f"📂 Found {len(images)} images — starting OCR extraction...")

for idx, image_name in enumerate(images, 1):
    image_path = os.path.join(folders_path, image_name)
    logging.info(f"🖼️ Processing {idx}/{len(images)}: {image_name}")

    try:
        with io.open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)

        if response.error.message:
            logging.error(f"❌ API Error for {image_name}: {response.error.message}")
            continue

        full_text = response.full_text_annotation.text.strip()
        if not full_text:
            logging.warning(f"⚠️ No text found in {image_name}")
            continue

        ocr_results[image_name] = full_text
        logging.info(f"✅ OCR text extracted from {image_name} ({len(full_text)} chars)")

        # small delay to avoid hitting rate limits
        time.sleep(2)

    except Exception:
        logging.exception(f"❌ Error processing {image_name}")

# ------------------------------------------------------------
# SAVE OCR OUTPUT
# ------------------------------------------------------------
# 1️⃣ Save per-page results to JSON
ocr_json_path = os.path.join(folders_path, "ocr_results.json")
with open(ocr_json_path, "w", encoding="utf-8") as f:
    json.dump(ocr_results, f, ensure_ascii=False, indent=4)
logging.info(f"💾 OCR results saved to {ocr_json_path}")

# 2️⃣ Save merged text to single TXT file
merged_txt_path = os.path.join(folders_path, "ocr_merged.txt")
with open(merged_txt_path, "w", encoding="utf-8") as f:
    for name in images:
        if name in ocr_results:
            f.write(f"===== {name} =====\n")
            f.write(ocr_results[name] + "\n\n")
logging.info(f"💾 Combined text saved to {merged_txt_path}")

logging.info("🏁 OCR extraction complete — all text saved.") 
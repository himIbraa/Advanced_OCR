import cv2
import numpy as np
import os
import glob

# === CONFIGURATION ===
input_folder = r"\media\criminal_procedures"
output_folder = r"\media\criminal_procedures_output"
os.makedirs(output_folder, exist_ok=True)

# 🔧 Adjust this value to control how much of the top is cropped (e.g., 0.03 = 3%, 0.05 = 5%)
HEADER_RATIO = 0.045

# === PROCESS EACH IMAGE ===
image_paths = sorted(glob.glob(os.path.join(input_folder, "*.png")))
if not image_paths:
    print(f"⚠️ No image files found in folder: {input_folder}")
else:
    for file_path in image_paths:
        page_name = os.path.splitext(os.path.basename(file_path))[0]
        img = cv2.imread(file_path)
        if img is None:
            print(f"❌ Could not read image: {file_path}")
            continue

        # --- Remove white borders ---
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
        coords = cv2.findNonZero(thresh)
        if coords is None:
            print(f"⚠️ Skipping blank image: {file_path}")
            continue

        x, y, w, h = cv2.boundingRect(coords)
        cropped = img[y:y + h, x:x + w]

        # --- Remove header by percentage ---
        header_height = int(cropped.shape[0] * HEADER_RATIO)
        cropped_no_header = cropped[header_height:, :]

        # --- Split into left/right halves ---
        height, width, _ = cropped_no_header.shape
        mid = width // 2
        left_half = cropped_no_header[:, :mid]
        right_half = cropped_no_header[:, mid:]

        # --- Save outputs --- 
        left_path = os.path.join(output_folder, f"{page_name}_left.png")
        right_path = os.path.join(output_folder, f"{page_name}_right.png")
        cv2.imwrite(left_path, left_half)
        cv2.imwrite(right_path, right_half)

        print(f"✅ Processed page {page_name}")

    print("\n🎉 All pages processed successfully!")

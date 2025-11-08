# 🏛️ Complete Decree OCR Pipeline

A comprehensive end-to-end solution for **extracting, processing, and recognizing text** from *official journal decree documents* using a **PDF-to-OCR pipeline** with full **Arabic language support**.

---

## 📋 Pipeline Overview

```
PDF Files
   ↓
[Step 1: PDF to PNG Converter] → Extract pages as images
   ↓
PNG Images (./media/{pdf_name}/)
   ↓
[Step 2: Decree Image Processor] → Remove headers, crop, split columns
   ↓
Processed Two-Column Images (./media/{pdf_name}_output/)
   ↓
[Step 3: Google Vision OCR] → Extract Arabic text (right→left)
   ↓
JSON + TXT Output (Structured & Merged Text)
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install all dependencies
pip install pdf2image opencv-python numpy google-cloud-vision jupyter

# System dependencies
# macOS:
brew install poppler

# Linux:
sudo apt-get install poppler-utils

# Windows:
pip install python-poppler-qt5
```

---

### Setup Google Cloud Vision

1. **Create Google Cloud Project**

   * Go to [Google Cloud Console](https://console.cloud.google.com/)
   * Create a new project
   * Enable the *Vision API*

2. **Create Service Account**

   * Navigate to **IAM & Admin → Service Accounts**
   * Create a new service account
   * Generate and download the JSON key
   * Place it as `credentials.json` in the project root directory

---

### Directory Structure

```
project_root/
├── Advanced_OCR.ipynb            # Main notebook (all steps)
├── credentials.json              # Google Cloud credentials
├── PDF/                          # Input PDFs
└── media/                        # Processing pipeline outputs
    ├── {pdf_name}/               # Original PNG extracts
    └── {pdf_name}_output/        # Processed two-column splits
        ├── {pdf_name}.json       # Structured OCR results
        └── {pdf_name}.txt        # Merged OCR text
```

---

## 📖 Notebook Usage

### Launch the Jupyter Notebook

```bash
jupyter notebook Advanced_OCR.ipynb
```

Open the notebook in your browser and run each cell sequentially to execute the pipeline.

---

## 🔧 Pipeline Steps (Inside Notebook)

### Step 1: PDF to PNG Converter

**Purpose:**

* Converts all PDFs in `./PDF/` to individual PNG pages
* Maintains 200 DPI quality (configurable)
* Logs progress, file size, and potential conversion errors

**Key Features:**

* ✅ Batch processing for multiple PDFs
* ✅ Organized output folders (`./media/{pdf_name}/`)
* ✅ Adjustable DPI for image clarity
* ✅ Progress and error logging

**Output:**
`./media/{pdf_name}/page_X.png` — ready for the next step.

---

### Step 2: Decree Image Processor

**Purpose:**

* Removes borders and headers
* Splits two-column pages intelligently
* Saves clean, ready-for-OCR images

**Key Features:**

* ✅ White border removal via contour detection
* ✅ Configurable header crop percentage (default 4.5%)
* ✅ Automatic two-column detection and split
* ✅ Batch processing with logs
* ✅ Maintains consistent naming convention

**Output:**
`./media/{pdf_name}_output/` — processed images, ready for OCR.

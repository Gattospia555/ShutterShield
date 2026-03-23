# 🛡️ ShutterShield
> **Protecting your pixels, erasing your footprints.**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Pillow](https://img.shields.io/badge/Pillow-Library-green?style=for-the-badge)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-GUI-darkblue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

## 📌 Project Description
**ShutterShield** is a lightweight Python GUI application designed to automatically strip sensitive EXIF metadata from your photos.

Whether you are a photographer sharing shots online or a user posting images on forums, cameras often embed GPS coordinates, timestamps, and device data in image files. ShutterShield works as a privacy firewall: it sanitizes folders of images in a few seconds, producing clean files without visible quality loss.

## ✨ Key Features
* **Smart Compression Retention:** Preserves the original JPEG quality and subsampling, and optimizes Huffman tables to prevent file size bloat while stripping data.
* **Batch & Single Processing:** Select a single photo or handle hundreds of images with multithreading while keeping the UI responsive.
* **Zero privacy leaks:** EXIF and GPS tags are securely wiped from all processed files.
* **Modern interface:** dark-mode GUI built with `CustomTkinter` and intuitive workflow.
* **Robust error handling:** corrupted or unsupported files are skipped without stopping the process.

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Gattospia555/ShutterShield.git
   ```

2. Change to the project directory:
   ```bash
   cd ShutterShield
   ```

3. Install dependencies (recommended in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Click **Select Single Photo** or **Select Photo Folder** to choose the image(s) to sanitize.
3. Click **Select Output Folder** to choose an output directory.
4. Click **Start Cleaning** and watch the progress bar.

*Note:* sanitized image(s) are saved with the `clean_` prefix in the filename.

## 📦 Included Files
* `app.py` - main GUI application with sanitization logic.
* `requirements.txt` - required dependencies (e.g. Pillow, CustomTkinter).

## 🔐 Why Privacy Matters
Uploading raw images to the internet can inadvertently leak your home address, daily routines, or the exact locations of your photo shoots (a classic OSINT vulnerability). ShutterShield prevents unintentional data leakage and location tracking by enforcing strict metadata sanitization before any file hits the web.

## 📝 License
Project released under the MIT License.

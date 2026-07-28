import io
import os
import requests
import fitz  # PyMuPDF

PDF_URL = "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/66/air-56-surabhi-srivastava_test-1_gs1.pdf"
OUTPUT_FILE = "compressed_surabhi_srivastava_gs1.pdf"

TARGET_MIN_MB = 45.0
TARGET_MAX_MB = 50.0

def compress_pdf_to_target():
    print("Fetching PDF into RAM...", flush=True)
    res = requests.get(PDF_URL)
    if res.status_code != 200:
        print(f"Failed to fetch file. Status: {res.status_code}")
        return

    original_size = len(res.content) / (1024 * 1024)
    print(f"Original File Size: {original_size:.2f} MB")

    # Load original bytes into RAM
    doc_raw = fitz.open(stream=io.BytesIO(res.content), filetype="pdf")

    # Start with high quality parameters to keep size above 45 MB
    dpi = 180
    quality = 80

    for attempt in range(1, 6):
        print(f"\n--- Attempt {attempt}: Testing parameters (DPI={dpi}, JPEG Quality={quality}) ---", flush=True)
        new_doc = fitz.open()

        for page_num in range(len(doc_raw)):
            page = doc_raw[page_num]
            # Render page at controlled DPI
            pix = page.get_pixmap(dpi=dpi)
            
            # Convert to JPEG bytes at controlled quality
            img_bytes = pix.tobytes("jpeg", jpg_quality=quality)

            # Create new page matching original dimensions
            rect = page.rect
            new_page = new_doc.new_page(width=rect.width, height=rect.height)
            new_page.insert_image(rect, stream=img_bytes)

        # Save trial output
        new_doc.save(OUTPUT_FILE, garbage=4, deflate=True)
        new_doc.close()

        current_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
        print(f"Generated File Size: {current_size_mb:.2f} MB")

        # Adjust parameters if size falls outside 45 MB - 50 MB
        if TARGET_MIN_MB <= current_size_mb <= TARGET_MAX_MB:
            print(f"\nSUCCESS! Target file size reached: {current_size_mb:.2f} MB")
            break
        elif current_size_mb > TARGET_MAX_MB:
            print("File is too large (> 50 MB). Lowering quality slightly...")
            quality -= 8
            dpi -= 10
        else:
            print("File is too small (< 45 MB). Increasing quality to maintain max clarity...")
            quality += 6
            dpi += 10

if __name__ == "__main__":
    compress_pdf_to_target()

import io
import requests
import fitz  # PyMuPDF

PDF_URL = "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/58/air-56-surabhi-srivastava_test-3_gs3.pdf"
OUTPUT_FILE = "compressed_surabhi_srivastava_gs3.pdf"

def compress_pdf_from_url(url, output_path):
    print("Downloading PDF into memory...", flush=True)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch PDF. Status code: {response.status_code}")
        return

    original_size = len(response.content) / (1024 * 1024)
    print(f"Original File Size: {original_size:.2f} MB")

    # Load bytes directly into memory
    pdf_stream = io.BytesIO(response.content)
    doc = fitz.open(stream=pdf_stream, filetype="pdf")

    print(f"Compressing {len(doc)} pages...", flush=True)

    # Save with garbage collection, object deduplication, stream compression, and image downscaling
    doc.save(
        output_path,
        garbage=4,          # Remove unused objects
        deflate=True,        # Compress uncompressed streams
        deflate_images=True, # Re-compress embedded raster images
        clean=True           # Sanitize and optimize page content
    )
    doc.close()

    # Calculate compressed size
    import os
    compressed_size = os.path.getsize(output_path) / (1024 * 1024)
    reduction = ((original_size - compressed_size) / original_size) * 100

    print(f"\nCompression Complete!")
    print(f"New File Size: {compressed_size:.2f} MB")
    print(f"Size Reduced By: {reduction:.1f}%")

if __name__ == "__main__":
    compress_pdf_from_url(PDF_URL, OUTPUT_FILE)

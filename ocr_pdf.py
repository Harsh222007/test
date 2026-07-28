import os
import requests
import fitz  # PyMuPDF
import google.generativeai as genai

# 1. Setup API key
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

PDF_URL = "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/58/air-56-surabhi-srivastava_test-3_gs3.pdf"
PDF_FILE = "surabhi_srivastava_gs3.pdf"
OUTPUT_MD = "surabhi_srivastava_gs3_transcribed.md"

def transcribe_handwritten_pdf():
    # Download PDF
    print("Downloading PDF...")
    res = requests.get(PDF_URL)
    with open(PDF_FILE, "wb") as f:
        f.write(res.content)

    doc = fitz.open(PDF_FILE)
    print(f"Total Pages: {len(doc)}")

    prompt = """
    You are an expert OCR and document transcriber. 
    Transcribe this handwritten UPSC General Studies answer sheet into clean, highly structured Markdown.
    
    Formatting rules:
    1. Preserve all question numbers, sub-parts, headings, and bullet points.
    2. Use **bold** for underlined or emphasized handwritten text.
    3. If there are hand-drawn diagrams or flowcharts, describe them concisely using blockquotes or standard text boxes, or format them as ASCII diagrams/tables.
    4. Maintain readable paragraph structure without correcting the author's original legal/factual phrasing.
    """

    full_markdown = []

    for idx, page in enumerate(doc, 1):
        print(f"Processing page {idx}/{len(doc)}...")
        
        # Render PDF page to PNG image in memory
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes("png")

        # Send image to Gemini Vision model
        image_part = {"mime_type": "image/png", "data": img_bytes}
        response = model.generate_content([prompt, image_part])

        page_text = f"\n\n<!-- PAGE {idx} START -->\n\n" + response.text
        full_markdown.append(page_text)

    # Save to Markdown
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.writelines(full_markdown)

    print(f"Done! Saved full transcription to '{OUTPUT_MD}'")

if __name__ == "__main__":
    transcribe_handwritten_pdf()

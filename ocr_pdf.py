import io
import os
import sys
import requests
import fitz  # PyMuPDF
from google import genai
from google.genai import types

# 1. Initialize client using modern Google GenAI SDK
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable is missing.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

PDF_URL = "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/58/air-56-surabhi-srivastava_test-3_gs3.pdf"
OUTPUT_MD = "surabhi_srivastava_gs3_transcribed.md"

def transcribe_pdf_in_memory():
    print(f"Streaming PDF directly into RAM from URL...")
    res = requests.get(PDF_URL)
    if res.status_code != 200:
        print(f"Failed to fetch PDF. HTTP Status: {res.status_code}")
        sys.exit(1)

    # Load bytes directly into memory (PyMuPDF stream)
    pdf_stream = io.BytesIO(res.content)
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    print(f"Successfully loaded PDF into memory! Total Pages: {len(doc)}")

    prompt = """
    You are an expert handwritten document transcriber.
    Transcribe this handwritten UPSC General Studies answer sheet page into clean, highly structured Markdown.
    
    Rules:
    1. Preserve all question numbers, sub-parts, headings, and bullet points.
    2. Use **bold** for underlined or highlighted handwritten words.
    3. If there are hand-drawn diagrams, flowcharts, or tables, represent them as ASCII diagrams or Markdown tables.
    4. Do not summarize or alter the original content.
    """

    full_markdown = []

    for idx, page in enumerate(doc, 1):
        print(f"Processing Page {idx}/{len(doc)}...", flush=True)
        
        # Render PDF page to PNG image bytes strictly in RAM
        pix = page.get_pixmap(dpi=150)
        png_bytes = pix.tobytes("png")

        try:
            # Send image directly from RAM buffer to Gemini 3 Flash
            response = client.models.generate_content(
                model='gemini-3-flash',
                contents=[
                    types.Part.from_bytes(
                        data=png_bytes,
                        mime_type='image/png',
                    ),
                    prompt
                ]
            )

            page_text = f"\n\n<!-- PAGE {idx} START -->\n\n" + (response.text or "")
            full_markdown.append(page_text)
        except Exception as e:
            print(f"   --> Error on Page {idx}: {e}", flush=True)

    # Save final transcribed Markdown file
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.writelines(full_markdown)

    print(f"\nSuccess! Transcribed document generated: '{OUTPUT_MD}'")

if __name__ == "__main__":
    transcribe_pdf_in_memory()

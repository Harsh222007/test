import io
import sys
import requests
from pypdf import PdfWriter

NEXT_IAS_URLS = [
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/17/air-60-abhimanyu-malik_test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/139/air-43-thakur-anjali-ajay_test-8_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/022c58f3f0988adf83a584c53e9d0ac5/112/pttp220600_tc074-test-04-gs-04.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/93393beb2b7e996905ce7ea7f8b78443/66/air-79-eshani-anand_test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/52/air-50-k-n-chandana-jahnavi_test-8_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/93393beb2b7e996905ce7ea7f8b78443/50/air-11-kush-motwani_test-8_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/93393beb2b7e996905ce7ea7f8b78443/59/air-11-kush-motwani_test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/93393beb2b7e996905ce7ea7f8b78443/64/air-88-manan-bhat_test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/140/air-13-medha-anand_test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/35/air-53-mohan-lal__test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/93393beb2b7e996905ce7ea7f8b78443/100/air-9-nausheen_test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/93393beb2b7e996905ce7ea7f8b78443/93/air-9-nausheen_test-8_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/100/air-91-nidhi-goyal_test-8_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/93393beb2b7e996905ce7ea7f8b78443/88/air-69-priya-rani_test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/115/air-5-ruhani_test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/844233c60d0563afaf56a5f899c17647/4/pttp220996_tc063.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/93393beb2b7e996905ce7ea7f8b78443/80/air-77-shoham-teberiwal_test-8_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/93393beb2b7e996905ce7ea7f8b78443/10/air-95-srishti-mishra_test-12_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/49/air-56-surabhi-srivastava_test-8_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/64/air-56-surabhi-srivastava_test-4_gs4.pdf",
    "https://next-ias-appsquadz.s3.ap-south-1.amazonaws.com/file_library/pdf/original/ee21bf4c91767f03906ea17bc7230b10/11/air-31-vishnu-sasikumar_test-4_gs4.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/4/ethics-enhancer-test-1-ashi-sharma-1745407520398.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/4/ethics-enhancer-test-1-divyank-gupta-1745408736043.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/4/gs-mac-test-1-panchal-smit-1745409446939.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/5/abhishek-singh-test-19-1747312008450.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/5/abhishek-singh-test-20-1747312028825.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/5/abhishek-singh-test-21-1747312041888.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/5/abhishek-singh-test-23-1747312075479.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/5/ritika-test-11-1747228535045.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/5/ritika-test-13-1747226364895.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/5/ritika-test-14-1747226380860.pdf",
    "https://www.nextias.com/newuploads/Nextias/2025/5/ritika-test-6-1747228451975.pdf"
]

def merge_pdfs():
    merger = PdfWriter()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    downloaded_count = 0

    print(f"Starting download of {len(NEXT_IAS_URLS)} PDFs...", flush=True)

    for idx, url in enumerate(NEXT_IAS_URLS, 1):
        filename = url.split('/')[-1]
        try:
            print(f"[{idx}/{len(NEXT_IAS_URLS)}] Fetching: {filename}", flush=True)
            res = requests.get(url, headers=headers, timeout=30)
            if res.status_code == 200:
                merger.append(io.BytesIO(res.content))
                downloaded_count += 1
            else:
                print(f"   --> HTTP Error {res.status_code}", flush=True)
        except Exception as e:
            print(f"   --> Error: {e}", flush=True)

    if downloaded_count == 0:
        print("Error: No PDFs were successfully downloaded!", flush=True)
        sys.exit(1)

    output_filename = "Next_IAS_GS4_Merged.pdf"
    with open(output_filename, "wb") as f_out:
        merger.write(f_out)
    
    print(f"\nSuccess! Saved {downloaded_count} PDFs into '{output_filename}'", flush=True)

if __name__ == "__main__":
    merge_pdfs()

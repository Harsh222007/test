import io
import sys
import requests
from pypdf import PdfWriter

# List of all 54 Vision IAS PDF URLs
VISION_IAS_URLS = [
    "https://cdn.visionias.in/toppersanswerbooklet/145c9-1142925_4513_aakash_om_trivedi_rank_73.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/93c7a-305150_2220_abhinav-siwach-rank-12.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/32c5c-45845653_4513_abhishek_chauhan_rank_102.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/a22df-1216850_4513_aditya_mathur_rank_98.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/506d4-00315413_4513_aditya_narayan_h_rank_68.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/9cb98-661968_2931_akansh_dhull_rank_03.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/0ee89-661968_4513_akansh_dhull_rank_03.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/0880c-45866015_2716_akshit_bhardwaj_rank_12.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/b49e1-45866015_3612_akshit_bhardwaj_rank_12.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/2c91f-1055139_4513_ananya_rana_rank_60.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/807d5-1305363_3612_animesh_jain_rank_63.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/d70d5-623655_4513_apurva-verma_rank_42.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/48cd5-1138117_2070_dongre_archit_parag_rank_03.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/cfdc4-1138117_2425_dongre_archit_parag_rank_03.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/6ccf8-719762_2220_arfa-usmani_rank_124.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/872d7-1537720_4513_aryan_yadav_rank_31.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/c9647-1217831_2425_bhavika_chopra_rank_25.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/36644-1217831_4513_bhavika_chopra_rank_25.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/8ef5d-1343696_2931_bipul-gupta_rank_103.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/8e72b-365537_2421_deeksha_chourasiya_rank_44.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/ca565-365537_2425_deeksha_chourasiya_rank_44.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/96994-1467775_4513_deeksha_patkar_rank_88.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/e9f5b-859046_1830_devansh_gupta_rank_77.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/76e25-45883336_3612_devyanshi_kaura_rank_71.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/04dd5-1138476_2931_nisar_dishant_amrutlal_rank_19.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/35119-346699_2370_gudelli_srujana_rank_55.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/5d8e4-346699_2366_gudelli_srujana_rank_55.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/6d76b-1387488_4513_harsh_nehara_rank_74.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/9f6fc-874484_4513_alase_hrishikesh_rajendra_rank_61.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/7e533-46007892_4513_ishan_bhatnagar_rank_05.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/b74e6-45885442_4513_ishitwa_anand_rank_50.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/c3bfe-1528536_4513_jayant_garg_rank_64.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/7823e-1178032_1827_kanishak_aggarwal_rank_72.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/d7c8d-1012764_4513_kiran_kamate_rank_53.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/072dd-1293391_2070_manika-gupta_rank_127.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/256a9-709839_2359_mansi-singh_rank_126.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/7bb05-115128_2078_monika_srivastava_rank_16.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/8c9b1-115128_4513_monika_srivastava_rank_16.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/d2de8-1344988_2425_nikita_verma_rank_30.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/a9ecb-1009670_2070_pakshal_secretry_rank_08.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/ece82-1009670_2092_pakshal_secretry_rank_08.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/d8a9a-900058_2931_pawan-kumar-pandey_rank_138.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/c11de-1051591_1827_priyanka_choudhary_rank_79.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/7b7e2-1051591_1830_priyanka_choudhary_rank_79.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/c74df-430778_1416_rahul-kumar_rank_141.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/8a8d5-45942651_2720_rakhi_rank_65.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/df294-46054445_4513_rasneet_kaur_rank_51.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/17930-1378810_2487_rupal_jaiswal_rank_43.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/0deab-01430179_4513_samiksha_dwivedi_rank_56.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/8f29e-1430179_2716_samiksha_dwivedi_rank_56.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/7090f-475600_1227_sattwik_satyakam_devta_rank_100.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/dc354-1068271_2088_saurabh-sharma_rank_146.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/a7a9a-1158734_2931_simrandeep_kaur_rank_14.pdf",
    "https://cdn.visionias.in/toppersanswerbooklet/afc4b-1158734_4513_simrandeep_kaur_rank_14.pdf"
]

def merge_pdfs():
    merger = PdfWriter()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    downloaded_count = 0

    print(f"Starting download of {len(VISION_IAS_URLS)} Vision IAS PDFs...", flush=True)

    for idx, url in enumerate(VISION_IAS_URLS, 1):
        filename = url.split('/')[-1]
        try:
            print(f"[{idx}/{len(VISION_IAS_URLS)}] Fetching: {filename}", flush=True)
            res = requests.get(url, headers=headers, timeout=30)
            if res.status_code == 200:
                merger.append(io.BytesIO(res.content))
                downloaded_count += 1
            else:
                print(f"   --> HTTP Error {res.status_code}", flush=True)
        except Exception as e:
            print(f"   --> Error downloading: {e}", flush=True)

    if downloaded_count == 0:
        print("Error: No PDFs were successfully downloaded!", flush=True)
        sys.exit(1)

    output_filename = "Vision_IAS_GS4_Merged.pdf"
    with open(output_filename, "wb") as f_out:
        merger.write(f_out)
    
    print(f"\nSuccess! Merged {downloaded_count} Vision IAS PDFs into '{output_filename}'", flush=True)

if __name__ == "__main__":
    merge_pdfs()

import datetime

# ====== Bảng dịch địa danh Việt → Anh ======
translations = {
    "Đường": "St",
    "Phố": "Street",
    "Thôn": "Village",
    "Ấp": "Hamlet",
    "Xóm": "Hamlet",
    "Xã": "Commune",
    "Phường": "Ward",
    "Quận": "District",
    "Huyện": "District",
    "Thị trấn": "Town",
    "Thành phố": "City",
    "Tỉnh": "Province",
    "Khu phố": "Quarter",
    "Khu": "Area",
    "Khu công nghiệp": "Industrial Zone",
    "Cảng": "Port",
    "Sân bay": "Airport"
}

# ====== Bảng dịch ngành nghề Việt → Anh ======
industry_translations = {
    "Xây Dựng": "Construction",
    "Thương Mại": "Trading",
    "Dịch Vụ": "Services",
    "Sản Xuất": "Manufacturing",
    "Du Lịch": "Tourism",
    "Vận Tải": "Transport",
    "Nông Nghiệp": "Agriculture",
    "Công Nghệ": "Technology",
    "Y Tế": "Healthcare",
    "Giáo Dục": "Education",
    "Tài Chính": "Finance"
}

def format_title_case(text):
    return " ".join([w.capitalize() for w in text.split()])

def process_company_name(raw_name):
    name = format_title_case(raw_name)
    name = name.replace("Trách Nhiệm Hữu Hạn", "TNHH").replace("Cổ Phần", "CP")
    return name

def translate_company_name(name):
    parts = name.split()
    company_type = ""
    if "TNHH" in parts:
        company_type = "Co Ltd"
        parts.remove("TNHH")
    elif "CP" in parts:
        company_type = "JSC"
        parts.remove("CP")

    industry = ""
    for vn, en in industry_translations.items():
        if vn in name:
            industry = en
            parts = [p for p in parts if p != vn]
            break

    parts = [p for p in parts if p.lower() not in ["công", "ty"]]
    proper_name = " ".join(parts)
    eng_name = f"{proper_name} {industry} {company_type}".strip()
    return format_title_case(eng_name)

def extract_address(raw_address, mode="street"):
    parts = raw_address.split(",")
    if mode == "street":
        filtered = [p for p in parts if any(k in p.lower() for k in ["đường","thôn","ấp","xóm"])]
    elif mode == "ward":
        filtered = [p for p in parts if any(k in p.lower() for k in ["xã","phường","thị trấn"])]
    else:
        filtered = []
    return format_title_case(", ".join(filtered))

def translate_address(address):
    eng = format_title_case(address)
    for vn, en in translations.items():
        eng = eng.replace(vn, en)
    return eng

def process_data(raw_name, raw_address, phone, director):
    today = datetime.date.today()
    company_name = process_company_name(raw_name)
    company_name_eng = translate_company_name(company_name)
    addr1 = extract_address(raw_address, "street")
    addr1_eng = translate_address(addr1)
    addr2 = extract_address(raw_address, "ward")
    addr2_eng = translate_address(addr2)
    director_name = format_title_case(director)

    summary = f"【{today.day}/{today.month}/{today.year}; Phone: {phone}; Checked firm: Director & address OK】"

    return {
        "Trường 1": company_name,
        "Trường 2": company_name_eng,
        "Trường 3": addr1,
        "Trường 4": addr1_eng,
        "Trường 5": addr2,
        "Trường 6": addr2_eng,
        "Trường 7": phone,
        "Trường 8": director_name,
        "Trường 9": summary
    }
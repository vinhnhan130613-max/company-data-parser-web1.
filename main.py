import re
import datetime

# Bảng dịch địa danh
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
    "TP": "City",
    "Tỉnh": "Province"
}

# Bảng dịch ngành nghề
industry_translations = {
    "Xây Dựng": "Construction",
    "Giải Pháp": "Solutions",
    "Môi Trường": "Environment",
    "Nước": "Water",
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
            break

    parts = [p for p in parts if p.lower() not in ["công", "ty"]]
    proper_name = " ".join(parts)
    eng_name = f"{proper_name} {industry} {company_type}".strip()
    return format_title_case(eng_name)

def translate_address(address):
    eng = format_title_case(address)
    for vn, en in translations.items():
        eng = eng.replace(vn, en)
    return eng

def parse_raw_data(text):
    result = {}

    # Trường 1: tên công ty
    match_name = re.search(r"CÔNG TY[^\n]+", text)
    if match_name:
        result["Trường 1"] = match_name.group(0).strip()
        result["Trường 2"] = translate_company_name(result["Trường 1"])

    # Trường 3 và 5: từ địa chỉ thuế
    match_addr_tax = re.search(r"Địa chỉ Thuế\s+([^\n]+)", text)
    if match_addr_tax:
        addr_tax = match_addr_tax.group(1).strip()
        street = addr_tax.split(",")[0]
        result["Trường 3"] = street
        result["Trường 4"] = translate_address(street)

        ward_match = re.search(r"Phường\s+[^\n,]+", addr_tax)
        if ward_match:
            result["Trường 5"] = ward_match.group(0)
            result["Trường 6"] = translate_address(result["Trường 5"])

    # Trường 7: điện thoại
    match_phone = re.search(r"Điện thoại\s+([0-9\.]+)", text)
    if match_phone:
        result["Trường 7"] = match_phone.group(1).replace(".", "")

    # Trường 9: người đại diện
    match_rep = re.search(r"Người đại diện\s+([^\n]+)", text)
    if match_rep:
        rep_name = format_title_case(match_rep.group(1).strip())
        result["Trường 8"] = rep_name
        today = datetime.date.today()
        result["Trường 9"] = f"【{today.day}/{today.month}/{today.year}; Phone: {result.get('Trường 7','')}; Checked firm: {rep_name} & address OK】"

    return result

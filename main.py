import re
import datetime
import unidecode

def format_title_case(text: str) -> str:
    """Viết hoa chữ cái đầu mỗi từ."""
    return " ".join([w.capitalize() for w in text.split()])

# Bảng từ khóa chung Việt → Anh (mở rộng)
COMMON_WORDS = {
    "ĐẦU TƯ": "Investment",
    "PHÁT TRIỂN": "Development",
    "KỸ THUẬT": "Technical",
    "THƯƠNG MẠI": "Trading",
    "SẢN XUẤT": "Manufacturing",
    "GIẢI PHÁP": "Solutions",
    "ĐIỆN MÁY": "Electrical Equipment",
    "GIA DỤNG": "Home Appliance",
    "CÔNG NGHỆ": "Technology",
    "DỊCH VỤ": "Services",
    "XÂY DỰNG": "Construction",
    "NƯỚC": "Water",
    "MÔI TRƯỜNG": "Environmental",
    "THANH TOÁN": "Payment",
    "QUỐC TẾ": "International",
    "ĐIỆN TỬ": "Electronics",
    "THỰC PHẨM": "Food",
    "NÔNG SẢN": "Agricultural Products",
    "XUẤT NHẬP KHẨU": "Import Export",
    "LOGISTICS": "Logistics",
    "BẢO HIỂM": "Insurance",
    "NGÂN HÀNG": "Bank",
    "TÀI CHÍNH": "Finance",
    "BẤT ĐỘNG SẢN": "Real Estate",
    "DU LỊCH": "Tourism",
    "GIÁO DỤC": "Education",
    "Y TẾ": "Healthcare",
    "VẬN TẢI": "Transportation",
    "NĂNG LƯỢNG": "Energy",
    "DẦU KHÍ": "Petroleum",
}

def translate_company_name(name: str) -> str:
    """
    Dịch tên công ty sang tiếng Anh theo nội dung.
    - TNHH -> Co Ltd
    - CP (Cổ Phần) -> JSC
    - Việt Nam -> Vietnam
    - Từ khóa chung dịch theo COMMON_WORDS
    - Tên riêng giữ nguyên (bỏ dấu, viết hoa chữ cái đầu)
    """
    name_clean = name.upper()

    company_type = ""
    if "TNHH" in name_clean:
        company_type = "Co Ltd"
    elif "CỔ PHẦN" in name_clean or "CP" in name_clean:
        company_type = "JSC"

    eng_name = name_clean.replace("VIỆT NAM", "Vietnam")
    eng_name = eng_name.replace("CÔNG TY TNHH", "").replace("CÔNG TY CỔ PHẦN", "").strip()

    words = eng_name.split()
    translated_words = []
    for w in words:
        if w in COMMON_WORDS:
            translated_words.append(COMMON_WORDS[w])
        else:
            translated_words.append(unidecode.unidecode(w).title())

    return " ".join(translated_words) + f" {company_type}"

def translate_segment(segment: str) -> str:
    """Dịch từng thành phần địa chỉ trong Trường 3."""
    seg = segment.strip()
    if seg.startswith("Đường"):
        return unidecode.unidecode(seg.replace("Đường", "").strip()) + " St"
    elif seg.startswith("Khu phố"):
        return unidecode.unidecode(seg.replace("Khu phố", "").strip()) + " Quarter"
    elif seg.startswith("Thôn"):
        return unidecode.unidecode(seg.replace("Thôn", "").strip()) + " Village"
    elif seg.startswith("Ấp"):
        return unidecode.unidecode(seg.replace("Ấp", "").strip()) + " Hamlet"
    else:
        return unidecode.unidecode(seg)

def translate_area(area: str) -> str:
    """Dịch phường/xã sang tiếng Anh."""
    area = area.strip()
    if area.startswith("Phường"):
        name = area.replace("Phường", "").strip()
        return unidecode.unidecode(name) + " Ward"
    elif area.startswith("Xã"):
        name = area.replace("Xã", "").strip()
        return unidecode.unidecode(name) + " Commune"
    return unidecode.unidecode(area)

def parse_raw_data(text: str) -> dict:
    result = {}

    # Trường 1–2
    match_name = re.search(r"(CÔNG TY[^\n]+|VĂN PHÒNG[^\n]+)", text)
    if match_name:
        raw_name = match_name.group(0).strip()
        result["Trường 1"] = format_title_case(raw_name)
        result["Trường 2"] = translate_company_name(result["Trường 1"])

    # Trường 3–6
    match_addr_tax = re.search(r"Địa chỉ Thuế\s+([^\n]+)", text)
    if match_addr_tax:
        addr_tax = match_addr_tax.group(1).strip()
        # tách trước khi gặp Phường/Xã
        parts = re.split(r"(Phường\s+[^\n,]+|Xã\s+[^\n,]+)", addr_tax)
        before_area = parts[0].strip().rstrip(",")
        result["Trường 3"] = before_area

        # dịch từng segment trong Trường 3
        translated_segments = []
        for seg in before_area.split(","):
            translated_segments.append(translate_segment(seg))
        result["Trường 4"] = ", ".join(translated_segments)

        # Trường 5–6: phường/xã
        if len(parts) > 1:
            area = parts[1].strip().rstrip(",")
            result["Trường 5"] = area
            result["Trường 6"] = translate_area(area)

    # Trường 7
    match_phone = re.search(r"Điện thoại\s+([0-9\s\.]+)", text)
    if match_phone:
        phone = match_phone.group(1).replace(".", "").replace(" ", "")
        result["Trường 7"] = phone if phone else "N/A"
    else:
        result["Trường 7"] = "N/A"

    # Trường 8–9
    match_rep = re.search(r"Người đại diện\s+([^\n]+)", text)
    if match_rep:
        rep_name = format_title_case(match_rep.group(1).strip())
        result["Trường 8"] = rep_name
        today = datetime.date.today()
        result["Trường 9"] = f"【{today.day}/{today.month}/{today.year}; Phone: {result.get('Trường 7','N/A')}; Checked firm: {rep_name} & address OK】"

    return result

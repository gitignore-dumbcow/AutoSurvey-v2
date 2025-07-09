import re

def sanitize_filename(name):
    """Loại bỏ ký tự đặc biệt và thay khoảng trắng bằng gạch dưới"""
    name = name.strip()
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name

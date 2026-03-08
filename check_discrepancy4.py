import json
from datetime import datetime

try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception:
    with open('data.js', 'r', encoding='utf-8') as f:
        content = f.read()
        start = content.find('const RAW_DATA = [')
        json_str = content[start + 17 : content.rfind('];') + 1]
        data = json.loads(json_str)

cnt = 0
amt = 0
for r in data:
    d = r.get("입력일", "")[:10]
    if "2025-12-01" <= d <= "2025-12-31":
        reg = r.get("지역제한", "")
        jong = r.get("종목", "")
        if ("서울" in reg or "서울특별시" in reg) and "전기" in jong:
            if "전국" not in reg:
                cnt += 1
                amt += r.get("추정가격", 0)

print(f"Only Seoul (no nationwide) and Electric in Dec 2025: Count={cnt}, Amount={amt:,}")

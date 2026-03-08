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

# Dec 2025 filter
filtered = []
for r in data:
    date_str = r.get("입력일", "")[:10]
    if "2025-12-01" <= date_str <= "2025-12-31":
        filtered.append(r)

# Seoul & Electric filter
seoul_elec = []
for r in filtered:
    reg = r.get("지역제한", "")
    jong = r.get("종목", "")
    if "서울" in reg and "전기" in jong:
        seoul_elec.append(r)

# Calculate counts and sums
cnt = len(seoul_elec)
amt = sum(r.get("추정가격", 0) for r in seoul_elec)

print(f"[Using 입력일 (Input Date)]")
print(f"Count: {cnt}")
print(f"Amount: {amt:,}")

# Let's also check using 공고일자 (Notice Date) just in case
filtered_notice = []
for r in data:
    date_str = r.get("공고일자", r.get("공고일", ""))[:10]
    if "2025-12-01" <= date_str <= "2025-12-31":
        filtered_notice.append(r)

seoul_elec_notice = []
for r in filtered_notice:
    reg = r.get("지역제한", "")
    jong = r.get("종목", "")
    if "서울" in reg and "전기" in jong:
        seoul_elec_notice.append(r)

cnt_notice = len(seoul_elec_notice)
amt_notice = sum(r.get("추정가격", 0) for r in seoul_elec_notice)

print(f"\\n[Using 공고일자 (Notice Date)]")
print(f"Count: {cnt_notice}")
print(f"Amount: {amt_notice:,}")

# Let's see category and region matching exactly as in JS
cnt_js = 0
amt_js = 0

for r in filtered:
    reg = r.get("지역제한", "")
    jong = r.get("종목", "")
    
    # JS Region Logic
    reg_hit = False
    if "서울" in reg: reg_hit = True
    
    # JS Category Logic (종목: 전기)
    # JS checks if any of ["전기"] is in jong
    cat_hit = False
    if "전기" in jong: cat_hit = True
    
    if reg_hit and cat_hit:
        cnt_js += 1
        amt_js += r.get("추정가격", 0)

print(f"\\n[JS Logic Match based on 입력일]")
print(f"Count: {cnt_js}")
print(f"Amount: {amt_js:,}")


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

dec_data = [r for r in data if '2025-12-01' <= r.get('입력일', '')[:10] <= '2025-12-31']

seoul_elec = [r for r in dec_data if ('서울' in r.get('지역제한', '') or '서울특별시' in r.get('지역제한', '')) and '전기' in r.get('종목', '')]
pure_seoul = [r for r in seoul_elec if '전국' not in r.get('지역제한', '')]

unique_seoul_elec = {}
for r in seoul_elec:
    unique_seoul_elec[r.get('공고번호')] = r

unique_pure_seoul = {}
for r in pure_seoul:
    unique_pure_seoul[r.get('공고번호')] = r

print(f"Total Dec 2025: {len(dec_data)}")
print(f"Seoul + Electric (incl Nationwide): {len(seoul_elec)}")
print(f"Seoul + Electric (incl Nationwide) UNIQUE: {len(unique_seoul_elec)}")
print(f"Seoul + Electric (excl Nationwide): {len(pure_seoul)}")
print(f"Seoul + Electric (excl Nationwide) UNIQUE: {len(unique_pure_seoul)}")

print(f"Total Amount (excl Nationwide): {sum(r.get('추정가격', 0) for r in pure_seoul):,}")
print(f"Total Amount UNIQUE (excl Nationwide): {sum(r.get('추정가격', 0) for r in unique_pure_seoul.values()):,}")

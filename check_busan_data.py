import json
from datetime import datetime

try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception:
    import json
    with open('data.js', 'r', encoding='utf-8') as f:
        content = f.read()
        start = content.find('const RAW_DATA = [')
        if start != -1:
            json_str = content[start + 17:]
            end = json_str.rfind('];')
            if end != -1:
                json_str = json_str[:end + 1]
            data = json.loads(json_str)

dates = [row['입력일'][:10] for row in data]
latest_date_str = max(dates)
latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")

from dateutil.relativedelta import relativedelta
start_date = latest_date - relativedelta(months=12)

filtered_data = [
    r for r in data
    if "전기" in r.get("종목", "") and datetime.strptime(r["입력일"][:10], "%Y-%m-%d") > start_date
]

busan_only = [r for r in filtered_data if "부산" in r.get("지역제한", "")]
nationwide = [r for r in filtered_data if "전국" in r.get("지역제한", "")]
busan_and_nation = busan_only + [r for r in nationwide if r not in busan_only]

print(f"Total Electrical in 12 months: {len(filtered_data)}")
print(f"Busan specific: {len(busan_only)}")
print(f"Nationwide: {len(nationwide)}")
print(f"Busan + Nationwide: {len(busan_and_nation)}")

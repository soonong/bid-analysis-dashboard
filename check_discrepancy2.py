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

dates = [row['입력일'][:10] for row in data]
latest_date_str = max(dates)
latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")
print("Latest Date in DB:", latest_date_str)

def filter_by_date(r, m):
    d = datetime.strptime(r['입력일'][:10], "%Y-%m-%d")
    import dateutil.relativedelta
    start = latest_date - dateutil.relativedelta.relativedelta(months=m)
    return start < d <= latest_date

# Exact render logic in JS:
# const endDate = new Date(latestDate);
# const startDate = new Date(latestDate);
# startDate.setMonth(startDate.getMonth() - m);
# startDate.setDate(startDate.getDate() + 1);
# data = data.filter(r => d >= startDate && d <= endDate);

import calendar
def get_js_start_date(latest, m):
    y = latest.year
    month = latest.month - m
    while month <= 0:
        y -= 1
        month += 12
    d = latest.day
    _, last_day = calendar.monthrange(y, month)
    d = min(d, last_day)
    start = datetime(y, month, d)
    from datetime import timedelta
    start = start + timedelta(days=1)
    return start

for m in [3, 6, 12]:
    sd = get_js_start_date(latest_date, m)
    print(f"Period {m}m: {sd.strftime('%Y-%m-%d')} ~ {latest_date.strftime('%Y-%m-%d')}")

# User said: 25년 12월 1일부터 31일까지 "한달간" 172개 754억. 
# But maybe dashboard shows period=3 or period=1?
# Let's check Trend chart data for 2025-12.
cnt = 0
amt = 0
for r in data:
    d = datetime.strptime(r['입력일'][:10], "%Y-%m-%d")
    if d.year == 2025 and d.month == 12:
        reg = r.get("지역제한", "")
        jong = r.get("종목", "")
        if "서울" in reg and "전기" in jong:
            cnt += 1
            amt += r.get("추정가격", 0)

print(f"\\nTrend Chart Bucket (2025-12) for Seoul & Electric regardless of JS filtering nationwide:")
print(f"Count: {cnt}")
print(f"Amount: {amt:,}")

# In Trend chart, if nationwide is included:
cnt_trend_heatmap = 0
amt_trend_heatmap = 0
for r in data:
    d = datetime.strptime(r['입력일'][:10], "%Y-%m-%d")
    if d.year == 2025 and d.month == 12:
        reg = r.get("지역제한", "")
        jong = r.get("종목", "")
        
        # JS Heatmap logic added '전국' check recently, but Trend chart does NOT separate '전국' vs '지역'. 
        # Wait, Trend chart uses filters applied at the top level.
        # `data = filterData(data, currentFilters);`
        # filterData does:
        # if filters.regions is ['서울']:
        #     matched = filters.regions.some(fr => ... )
        #     if (!matched && !filters.regions.includes('전국')) return false;
        # So filterData KEEPS '전국' rows even if you only select '서울' (if the row has '전국').
        filters_regions = ['서울']
        matched = False
        parts = filters_regions[0].split(' ')
        parentVals = [parts[0]]
        hit = False
        if any(v in reg for v in parentVals): hit = True
        
        if hit or '전국' in reg:
            # Matches region filter
            if "전기" in jong:
                # Matches category filter
                cnt_trend_heatmap += 1
                amt_trend_heatmap += r.get("추정가격", 0)

print(f"\\nTrend Chart Bucket (2025-12) for Filtered Data (Region='서울', Category='전기') [includes 전국]:")
print(f"Count: {cnt_trend_heatmap}")
print(f"Amount: {amt_trend_heatmap:,}")


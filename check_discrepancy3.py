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

# Find 189 / 45.1B
# Let's filter by month = 12, year = 2025 based on 입력일
dec_data = []
for r in data:
    d_str = r.get("입력일", "")
    if len(d_str) >= 10:
        d = datetime.strptime(d_str[:10], "%Y-%m-%d")
        if d.year == 2025 and d.month == 12:
            dec_data.append(r)

def test_combination(region_names, cat_names):
    # filterData logic
    matched = []
    for r in dec_data:
        reg = r.get("지역제한", "")
        jong = r.get("종목", "")
        
        # Region Filter (index.html line ~982)
        if region_names:
            hit_reg = False
            for fr in region_names:
                parts = fr.split(' ')
                parent = parts[0]
                # simplification
                if parent in reg:
                    if len(parts) == 1:
                        hit_reg = True
                    else:
                        if " ".join(parts[1:]) in reg:
                            hit_reg = True
            if not hit_reg and "전국" not in region_names and "전국" not in reg:
                # wait, if `전국` is in reg, `!matched && !filters.regions.includes('전국')` -> if `전국` in reg it bypasses? No!
                # if (!matched && !filters.regions.includes('전국')) return false;
                # JS says: if (!matched && !filters.regions.includes('전국')) return false;
                # Wait! JS says: `if (!matched && !filters.regions.includes('전국')) return false;`
                # If `matched` is false, AND filters.regions does NOT include '전국', it returns false.
                # It means if the row doesn't match the selected region, it's EXCLUDED. 
                # What if the row HAS "전국"? 
                # JS: 
                # const regionText = row.지역제한 || '';
                # const matched = filters.regions.some(fr => { ... return true if matches ... });
                # if (!matched && !filters.regions.includes('전국')) return false;
                
                # So if `matched` is false, and user didn't select '전국', it returns false. 
                # This means EVEN IF the row is '전국' (regionText has '전국'), if user selected '서울', `matched` is false (because '서울' is not in '전국').
                # And user didn't check '전국' in filters. So it returns false! 
                # So it EXCLUDES '전국' rows unless user checked '전국'!
                pass

        # Let's write the EXACT filter string:
        
        # 지역 필터
        if region_names:
            hit_reg = False
            for fr in region_names:
                parts = fr.split(' ')
                parentVals = [parts[0]]
                if "서울" == parts[0]: parentVals = ["서울특별시", "서울"]
                if any(v in reg for v in parentVals):
                    if len(parts) == 1:
                        hit_reg = True
                    else:
                        sub = " ".join(parts[1:])
                        if sub in reg:
                            hit_reg = True
            # if (!matched && !filters.regions.includes('전국')) return false;
            if not hit_reg and "전국" not in region_names:
                continue

        # 종목 필터
        if cat_names:
            hit_cat = False
            for fc in cat_names:
                vals = [fc]
                if fc == "전기": vals = ["전기"]
                if any(v in jong for v in vals):
                    hit_cat = True
            if not hit_cat:
                continue
                
        matched.append(r)
    return matched

# Test "서울" and "전기"
filtered_1 = test_combination(["서울"], ["전기"])
cnt = len(filtered_1)
amt = sum(r.get("추정가격", 0) for r in filtered_1)
print(f"Option 1: Filter exactly '서울' and '전기': Count={cnt}, Amount={amt:,}")

# Find any combination that gives 189
cnt_only_seoul = 0
for r in dec_data:
    reg = r.get("지역제한", "")
    jong = r.get("종목", "")
    # strict seoul electric
    if ("서울" in reg or "서울특별시" in reg) and "전기" in jong:
        if "전국" not in reg: # pure
            cnt_only_seoul += 1

print(f"Only Seoul (no nationwide) and Electric: Count={cnt_only_seoul}")

# Let's count by day to see if there is any date shift issues
print("Daily counts for Seoul + Electric (strictly):")
import collections
days = collections.Counter()
for r in filtered_1:
    d = r.get("입력일", "")[:10]
    days[d] += 1
for d in sorted(days):
    print(d, days[d])

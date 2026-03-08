import json
from datetime import datetime

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

dec_data = [r for r in data if '2025-12-01' <= r.get('입력일', '')[:10] <= '2025-12-31']

# Seoul + Electric (inclusive of 全国)
seoul_elec_all = [
    r for r in dec_data 
    if ('서울' in r.get('지역제한', '') or '서울특별시' in r.get('지역제한', '')) 
    and '전기' in r.get('종목', '')
]

target_cnt = 172
target_amt = 75418481366

# Try filtering by non-zero price + '서울' instead of '서울/경기' etc?
cnt_pure_seoul = 0
amt_pure_seoul = 0
for r in seoul_elec_all:
    if r.get("지역제한", "").strip() in ["서울", "서울특별시"] and "전국" not in r.get("지역제한", ""):
        cnt_pure_seoul += 1
        amt_pure_seoul += r.get("추정가격", 0)

print(f"Exact string '서울' (no 172/75.4B?) : Count={cnt_pure_seoul}, Amount={amt_pure_seoul:,}")

# Let's write a small brute force or check common exclusions
# like missing 적격평가세부기준? Check contract method?
methods = set(r.get("계약방법", "") for r in seoul_elec_all)
for m in methods:
    subset = [r for r in seoul_elec_all if r.get("계약방법", "") != m]
    if len(subset) == target_cnt or sum(r.get("추정가격", 0) for r in subset) == target_amt:
        print("MATCH EXCLUDE METHOD:", m, len(subset), sum(r.get("추정가격", 0) for r in subset))

import collections
c = collections.Counter([r.get("지역제한") for r in seoul_elec_all])
for k, v in c.items():
    subset = [r for r in seoul_elec_all if r.get("지역제한") != k]
    if len(subset) == target_cnt or sum(r.get("추정가격", 0) for r in subset) == target_amt:
        print("MATCH EXCLUDE REGION:", k, len(subset), sum(r.get("추정가격", 0) for r in subset))

# What if user's '서울' search only means `지역제한 == '서울'` or `지역제한 == '전국'`?
seoul_or_nation = [r for r in seoul_elec_all if r.get("지역제한") in ["서울", "서울특별시", "전국"]]
print(f"Seoul exactly or Nationwide exactly: Count={len(seoul_or_nation)}, amount={sum(r.get('추정가격', 0) for r in seoul_or_nation):,}")

# What if user is only searching `종목 == '전기'` and NOT `전문소방/(전기소방,기계소방)` ?
pure_category = [r for r in seoul_elec_all if r.get("종목") == "전기"]
print(f"Exactly Category '전기': Count={len(pure_category)}, amount={sum(r.get('추정가격', 0) for r in pure_category):,}")

pure_seoul_exact = [r for r in pure_category if "전국" not in r.get("지역제한")]
print(f"Exactly Category '전기' and no nationwide: Count={len(pure_seoul_exact)}, amount={sum(r.get('추정가격', 0) for r in pure_seoul_exact):,}")

pure_category_nation = [r for r in seoul_elec_all if r.get("종목") == "전기" and r.get("지역제한") in ["서울", "서울특별시", "전국"]]
print(f"Exactly Category '전기' and (Exactly Seoul or Nationwide): Count={len(pure_category_nation)}, amount={sum(r.get('추정가격', 0) for r in pure_category_nation):,}")

# Wait, if exactly '전기' (NOT 전문소방) and exactly "서울" + "전국"? Count=172? let's see!

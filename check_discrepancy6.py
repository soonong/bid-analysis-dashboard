import json
from datetime import datetime

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

dec_data = [r for r in data if '2025-12-01' <= r.get('입력일', '')[:10] <= '2025-12-31']
pure_seoul = [r for r in dec_data if ('서울' in r.get('지역제한', '') or '서울특별시' in r.get('지역제한', '')) and '전국' not in r.get('지역제한', '') and '전기' in r.get('종목', '')]

non_zero = [r for r in pure_seoul if r.get('추정가격', 0) > 0]
print(f'Count excluding 0 price: {len(non_zero)}')

# what if the user is filtering region by exactly "서울특별시" and not "서울 "? 
seoul_exact = [r for r in dec_data if r.get('지역제한', '').strip() == '서울특별시' and '전기' in r.get('종목', '')]
print(f'Count exact "서울특별시": {len(seoul_exact)}')

seoul_exact_2 = [r for r in dec_data if r.get('지역제한', '').strip() == '서울' and '전기' in r.get('종목', '')]
print(f'Count exact "서울": {len(seoul_exact_2)}')

# Check 종목
elec_exact = [r for r in pure_seoul if r.get('종목', '').strip() == '전기']
print(f'Count exactly "전기" in pure_seoul: {len(elec_exact)}')

print("All 종목 for pure_seoul:")
from collections import Counter
c = Counter([r.get('종목', '') for r in pure_seoul])
for k, v in c.items():
    print(k, v)

print("All 지역제한 for pure_seoul:")
c2 = Counter([r.get('지역제한', '') for r in pure_seoul])
for k, v in c2.items():
    print(k, v)


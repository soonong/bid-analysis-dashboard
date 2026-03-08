import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

dec_data = [r for r in data if '2025-12-01' <= r.get('입력일', '')[:10] <= '2025-12-31']

# user's formula
user_rows = []
for r in dec_data:
    reg = r.get('지역제한', '')
    jong = r.get('종목', '')
    
    # "서울" in region means ANY region string that contains "서울" or "서울특별시"
    if ('서울' in reg or '서울특별시' in reg):
        # AND exactly "전기"
        if jong.strip() == '전기':
            user_rows.append(r)

print(f"User Formula: Count={len(user_rows)}, Amount={sum(r.get('추정가격', 0) for r in user_rows):,}")

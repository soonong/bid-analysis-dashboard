import json
import csv

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The user expects all items matching "서울" in their region, even if they have "전국" like "전국/서울".
dec_data = [r for r in data if '2025-12-01' <= r.get('입력일', '')[:10] <= '2025-12-31']
user_seoul_elec = []

for r in dec_data:
    reg = r.get('지역제한', '')
    jong = r.get('종목', '')
    
    if ('서울' in reg or '서울특별시' in reg):
        # The user's excel only contains exactly '전기'
        if jong.strip() == '전기':
            user_seoul_elec.append(r)

csv_file = '2025_12_Seoul_Electric_Corrected.csv'
if user_seoul_elec:
    keys = list(user_seoul_elec[0].keys())
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in user_seoul_elec:
            writer.writerow(r)
    
    print(f"Saved {len(user_seoul_elec)} rows to {csv_file}")
    print(f"Total Amount: {sum(r.get('추정가격', 0) for r in user_seoul_elec):,}")


import json, csv, os

print("data.json 로딩 중...")
with open('data.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

fields = ['공고번호', '추정가격', '지역제한', '종목', '특수실적', '계약방법', '적격평가세부기준', '입력일']

out_path = 'data_export.csv'
with open(out_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    for r in records:
        row = {k: ('' if r.get(k) is None else r.get(k, '')) for k in fields}
        writer.writerow(row)

print(f'완료: {len(records):,}건 → {out_path}')
print(f'파일크기: {os.path.getsize(out_path):,} bytes')
print()
print('--- 처음 3행 미리보기 ---')
print(','.join(fields))
for r in records[:3]:
    print(','.join(str('' if r.get(k) is None else r.get(k, '')) for k in fields))

import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

dec_data = [r for r in data if '2025-12-01' <= r.get('입력일', '')[:10] <= '2025-12-31']
print("Total Dashboard Bids for Dec 2025:", len(dec_data))

heatmapRegions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '전국']
heatmapCats = ['건축', '토목', '조경', '산업환경설비', '전기', '통신', '소방', '지반조성.포장', '금속창호.지붕건축물조립', '도장.습식.방수.석공', '조경식재.시설물', '수중.준설', '승강기.삭도', '기계가스설비', '가스난방', '실내건축', '철콘', '비계구조', '상.하수도', '철도궤도', '철강구조물']

# Matches data.js output we just updated
REGION_MAP = {
    "서울": ["서울"],
    "경기": ["광명", "부천", "시흥", "고양", "경기"],
    "인천": ["인천"],
    "충남": ["충남", "충청남도"],
    "충북": ["충북", "충청북도"],
    "전남": ["전남", "전라남도", "전국/전남"],
    "경북": ["경북", "경상북도", "전국/대구/경북", "울진"],
    "대구": ["대구"],
    "부산": ["부산"],
    "경남": ["경남", "경상남도"],
    "전북": ["전북", "전라북도"],
    "강원": ["강원", "강원특별자치도"],
    "울산": ["울산"],
    "광주": ["광주", "광주광역시"],
    "대전": ["대전"],
    "세종": ["세종", "세종특별자치시"],
    "제주": ["제주", "제주특별자치도"],
    "전국": ["전국"],
}

CATEGORY_MAP = {
    "건축": ["건축", "실내건축", "철콘", "금속창호지붕", "비계구조", "금속창호", "지붕건축물조립"],
    "토목": ["토목", "토건", "지반조성포장", "지반조성", "포장"],
    "조경": ["조경", "조경식재", "조경시설물", "조경식재시설물", "산림조합", "사방"],
    "산업환경설비": ["산업환경설비"],
    "전기": ["전기", "전기소방", "전기,지반조성포장", "전기,토목", "토건,전기"],
    "통신": ["통신"],
    "소방": ["소방", "전문소방", "전기소방", "일반소방", "기계소방"],
    "도장.습식.방수.석공": ["도장", "습식", "방수", "석공", "도장습식방수석공"],
    "수중.준설": ["수중", "준설", "수중준설"],
    "승강기.삭도": ["승강기", "삭도", "승강기삭도"],
    "기계가스설비": ["기계설비", "가스설비", "기계가스설비", "기계가스"],
    "가스난방": ["가스", "난방", "가스난방"],
    "기타": [],
}

missing_bids = []
heatmap_total = 0

for row in dec_data:
    reg = row.get('지역제한', '')
    jong = row.get('종목', '')
    
    matchedRegions = []
    if '전국' in reg:
        if '전국' in heatmapRegions:
            matchedRegions.append('전국')
    else:
        for r in heatmapRegions:
            if r == '전국': continue
            
            parts = r.split(' ') # logic from index.html
            parentVals = REGION_MAP.get(parts[0], [parts[0]])
            hit = False
            
            if any(v in reg for v in parentVals):
                if len(parts) == 1:
                    hit = True
                else:
                    sub = ' '.join(parts[1:])
                    if sub in reg:
                        hit = True
            if hit:
                matchedRegions.append(r)
                
    matchedCats = []
    jongList = [s.strip() for s in jong.replace('/', ',').replace('(', ',').replace(')', ',').split(',') if s.strip()]
    for c in heatmapCats:
        cVals = CATEGORY_MAP.get(c, [c])
        if any(v in jongList or jong == v for v in cVals):
            matchedCats.append(c)
            
    if len(matchedRegions) > 0 and len(matchedCats) > 0:
        heatmap_total += 1
    else:
        missing_bids.append({
            'bid': row.get('공고번호'),
            'reg': reg,
            'jong': jong,
            'reason': 'No Region Match' if len(matchedRegions) == 0 else 'No Category Match'
        })

print(f"Heatmap Total Count (calculated exactly like index.html): {heatmap_total}")
print(f"Missing (Not in Heatmap): {len(missing_bids)}")

import collections
reasons = collections.Counter([b['reason'] for b in missing_bids])
print(reasons)

print("\nExamples of Missing Categories:")
for b in [x for x in missing_bids if x['reason'] == 'No Category Match'][:15]:
    print(f"[{b['jong']}]")

print("\nExamples of Missing Regions:")
for b in [x for x in missing_bids if x['reason'] == 'No Region Match'][:15]:
    print(f"[{b['reg']}]")

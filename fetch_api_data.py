#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bidding2.kr API 다중 월 데이터 수집 → data.js 생성
- 기본: 최근 12개월치 월별로 수집 (개월 수는 인자로 조절 가능)
- 추정가격: 문자열 → 정수 변환
- 특수실적: 빈 문자열 → null 변환
사용법:
    python fetch_api_data.py          # 최근 12개월
    python fetch_api_data.py 3        # 최근 3개월
    python fetch_api_data.py 6        # 최근 6개월
"""

import urllib.request
import json
import os
import sys
from datetime import datetime, date
from calendar import monthrange

BASE_URL = "https://bidding2.kr/api2/module/consortiumAPI/searchBidDataByDate_get.php"
MODULE_KEY = "happy304"

# ── 수집 월 범위 계산 ─────────────────────────────────────
months_back = int(sys.argv[1]) if len(sys.argv) > 1 else 12
today = date.today()

# 수집할 월 목록 생성 (오래된 순)
month_ranges = []
for i in range(months_back - 1, -1, -1):
    year = today.year
    month = today.month - i
    while month <= 0:
        month += 12
        year -= 1
    last_day = monthrange(year, month)[1]
    start = f"{year}-{month:02d}-01"
    end   = f"{year}-{month:02d}-{last_day:02d}"
    month_ranges.append((start, end))

print(f"📅 수집 대상: {month_ranges[0][0]} ~ {month_ranges[-1][1]} ({len(month_ranges)}개월)")
print("=" * 60)

all_data = []

for start_date, end_date in month_ranges:
    print(f"\n📡 [{start_date} ~ {end_date}] 수집 중...")
    month_count = 0

    for page in range(1, 300):
        url = f"{BASE_URL}?moduleKey={MODULE_KEY}&startDate={start_date}&endDate={end_date}&page={page}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            if not data or data == []:
                break
            all_data.extend(data)
            month_count += len(data)
            print(f"  ✅ page={page}: {len(data)}건 (누계 {month_count}건)")
        except Exception as e:
            print(f"  ❌ page={page}: {e}")
            break

    print(f"  → 월 소계: {month_count}건")

print(f"\n{'='*60}")
print(f"📊 전체 수집: {len(all_data)}건")

# ── 데이터 정제 ───────────────────────────────────────────
clean_data = []
seen = set()  # 중복 공고번호 제거

for row in all_data:
    bid_no = row.get("공고번호", "")
    if bid_no and bid_no in seen:
        continue
    if bid_no:
        seen.add(bid_no)

    try:
        price = int(float(row.get("추정가격", 0) or 0))
    except (ValueError, TypeError):
        price = 0

    special = row.get("특수실적", None)
    if special == "" or special is None:
        special = None

    input_date = row.get("입력일", "")
    if " " in input_date:
        input_date = input_date.split(" ")[0]

    clean_data.append({
        "공고번호":  bid_no,
        "추정가격":  price,
        "지역제한":  row.get("지역제한", ""),
        "종목":      row.get("종목", ""),
        "특수실적":  special,
        "계약방법":  row.get("계약방법", ""),
        "적격평가세부기준": row.get("적격평가세부기준", None),
        "입력일":    input_date,
    })

# 입력일 오름차순 정렬
clean_data.sort(key=lambda r: r["입력일"])

print(f"✨ 중복 제거 후: {len(clean_data)}건")

actual_start = clean_data[0]["입력일"] if clean_data else month_ranges[0][0]
actual_end   = clean_data[-1]["입력일"] if clean_data else month_ranges[-1][1]

# ── JS 배열 생성 ──────────────────────────────────────────
def to_js_value(val):
    if val is None:
        return "null"
    if isinstance(val, int):
        return str(val)
    if isinstance(val, str):
        val = val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "")
        return f'"{val}"'
    return str(val)

lines = []
for row in clean_data:
    parts = []
    for key in ["공고번호", "추정가격", "지역제한", "종목", "특수실적", "계약방법", "적격평가세부기준", "입력일"]:
        parts.append(f"{key}: {to_js_value(row[key])}")
    lines.append("    { " + ", ".join(parts) + " }")

js_array = "var RAW_DATA = [\n" + ",\n".join(lines) + "\n];\n"

# ── 헬퍼 코드 (data.js 하단 공통) ────────────────────────
# 로직은 index.html에 내장되었으므로 여기서는 최소한의 호환성 코드만 유지할 수 있으나,
# 대시보드 단독 동작을 위해 data.js는 순수 데이터만 담도록 비워둡니다.
helper_code = ""

# ── data.js 저장 (기존 방식 유지) ─────────────────────────────────────────────
header_comment = f"""// 발주공고 데이터 ({actual_start} ~ {actual_end}, API 자동 수집 {months_back}개월)
// 수집일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// 총 {len(clean_data)}건
// 원본 API: {BASE_URL}?moduleKey={MODULE_KEY}&startDate={actual_start}&endDate={actual_end}&page=N

"""

full_content = header_comment + js_array + helper_code

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.js")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_content)

# ── data.json 저장 (브라우저 fetch() 용 - 빠른 로딩) ──────────────────────────
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(clean_data, f, ensure_ascii=False, separators=(',', ':'))

print(f"\n💾 data.js  저장 완료: {output_path}")
print(f"💾 data.json 저장 완료: {json_path}")
print(f"📁 data.js  크기: {os.path.getsize(output_path)/1024/1024:.1f}MB")
print(f"📁 data.json 크기: {os.path.getsize(json_path)/1024/1024:.1f}MB")
print(f"📅 수집 기간: {actual_start} ~ {actual_end}")
print(f"📊 총 데이터: {len(clean_data)}건")
print("\n✅ 완료! 브라우저에서 index.html을 새로고침하세요.")

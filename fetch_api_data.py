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
helper_code = '''
// ──────────────────────────────────────────────
// 지역 정규화 헬퍼
// ──────────────────────────────────────────────
const REGION_MAP = {
    "서울": ["서울"],
    "경기": ["광명", "부천", "시흥", "고양", "경기"],
    "인천": ["인천"],
    "충남": ["충남"],
    "충북": ["충북"],
    "전남": ["전남", "전국/전남"],
    "경북": ["경북", "전국/대구/경북", "울진"],
    "대구": ["대구"],
    "부산": ["부산"],
    "경남": ["경남"],
    "전북": ["전북"],
    "강원": ["강원"],
    "울산": ["울산"],
    "광주": ["광주", "광주광역시"],
    "대전": ["대전"],
    "세종": ["세종"],
    "제주": ["제주"],
    "전국": ["전국"],
};

// ──────────────────────────────────────────────
// 종목 정규화 헬퍼
// ──────────────────────────────────────────────
const CATEGORY_MAP = {
    "전기": ["전기", "전기소방", "전기,지반조성포장", "전기,토목", "토건,전기"],
    "토목": ["토목", "토건", "지반조성포장"],
    "건축": ["건축", "실내건축", "철콘", "금속창호지붕", "비계구조"],
    "통신": ["통신"],
    "소방": ["전문소방", "전기소방", "전문소방"],
    "기계가스": ["기계가스설비"],
    "도장방수": ["도장습식방수석공"],
    "기타": [],
};

// ──────────────────────────────────────────────
// 발주처 추출 헬퍼
// ──────────────────────────────────────────────
function extractClient(criteria) {
    if (!criteria) return "기타";
    if (criteria.includes("한국전력")) return "KEPCO(한전)";
    if (criteria.includes("한국토지주택")) return "LH 한국토지주택";
    if (criteria.includes("한국수력원자력")) return "한국수력원자력";
    if (criteria.includes("행자부")) return "행정자치부(행자부)";
    if (criteria.includes("조달청")) return "조달청";
    if (criteria.includes("국방부")) return "국방부";
    if (criteria.includes("한국농어촌공사")) return "한국농어촌공사";
    if (criteria.includes("한국수자원공사")) return "한국수자원공사";
    if (criteria.includes("인천국제공항")) return "인천국제공항공사";
    if (criteria.includes("국가철도공단")) return "국가철도공단";
    if (criteria.includes("한국도로공사")) return "한국도로공사";
    return "기타";
}

// ──────────────────────────────────────────────
// 데이터 계산 / 통계 생성
// ──────────────────────────────────────────────
function computeStats(data) {
    const total = data.length;
    const totalAmt = data.reduce((s, r) => s + (r.추정가격 || 0), 0);
    const hasSpecial = data.filter(r => r.특수실적).length;
    const clientCount = {};
    data.forEach(r => {
        const c = extractClient(r.적격평가세부기준);
        clientCount[c] = (clientCount[c] || 0) + 1;
    });
    const topClient = Object.entries(clientCount).sort((a, b) => b[1] - a[1])[0];
    return { total, totalAmt, hasSpecial, topClient, clientCount };
}

// 지역-종목 히트맵용 교차 집계
function computeHeatmap(data) {
    const regions = ["서울", "경기", "인천", "충남", "부산", "경북", "전국"];
    const categories = ["전기", "통신", "소방", "건축", "토목", "기계가스", "도장방수", "기타"];
    const matrix = {};
    regions.forEach(r => { matrix[r] = {}; categories.forEach(c => matrix[r][c] = 0); });

    data.forEach(row => {
        const regions_matched = [];
        if (row.지역제한) {
            const v = row.지역제한;
            for (const [rKey, rVals] of Object.entries(REGION_MAP)) {
                if (rVals.some(rv => v.includes(rv)) || v === "전국") {
                    if (v === "전국") {
                        if (!regions_matched.includes("전국")) regions_matched.push("전국");
                    } else if (!regions_matched.includes(rKey)) {
                        regions_matched.push(rKey);
                    }
                }
            }
        }
        if (regions_matched.length === 0) regions_matched.push("기타");

        const cats_matched = [];
        if (row.종목) {
            const v = row.종목;
            for (const [cKey, cVals] of Object.entries(CATEGORY_MAP)) {
                if (cVals.some(cv => v.includes(cv))) {
                    if (!cats_matched.includes(cKey)) cats_matched.push(cKey);
                }
            }
        }
        if (cats_matched.length === 0) cats_matched.push("기타");

        regions_matched.forEach(r => {
            cats_matched.forEach(c => {
                if (matrix[r] !== undefined && matrix[r][c] !== undefined) {
                    matrix[r][c]++;
                }
            });
        });
    });
    return { matrix, regions, categories };
}

// ──────────────────────────────────────────────
// Filter helpers
// ──────────────────────────────────────────────
function filterData(data, filters) {
    return data.filter(row => {
        if (filters.regions && filters.regions.length > 0) {
            const regionText = row.지역제한 || '';
            const matched = filters.regions.some(fr => {
                const parts = fr.split(' ');
                if (parts.length >= 2 && REGION_MAP[parts[0]]) {
                    const parentRegion = parts[0];
                    const subDistrict = parts.slice(1).join(' ');
                    const parentRVals = REGION_MAP[parentRegion] || [parentRegion];
                    const parentMatched = parentRVals.some(rv => regionText.includes(rv));
                    if (!parentMatched) return false;
                    const regionTokens = regionText.split(/[\\/\\s,]+/);
                    return regionTokens.some(token => token.trim() === subDistrict);
                }
                const rVals = REGION_MAP[fr] || [fr];
                return rVals.some(rv => regionText.includes(rv));
            });
            if (!matched && !filters.regions.includes("전국")) return false;
        }
        if (filters.categories && filters.categories.length > 0) {
            const matched = filters.categories.some(fc => {
                const cVals = CATEGORY_MAP[fc] || [fc];
                return row.종목 && cVals.some(cv => row.종목.includes(cv));
            });
            if (!matched) return false;
        }
        if (filters.clients && filters.clients.length > 0) {
            const c = extractClient(row.적격평가세부기준);
            if (!filters.clients.includes(c)) return false;
        }
        if (filters.specialOnly) {
            if (!row.특수실적) return false;
        }
        if (filters.contractMethod) {
            if (row.계약방법 !== filters.contractMethod) return false;
        }
        if (filters.minAmt) {
            if ((row.추정가격 || 0) < filters.minAmt) return false;
        }
        if (filters.maxAmt) {
            if ((row.추정가격 || 0) > filters.maxAmt) return false;
        }
        return true;
    });
}

// ──────────────────────────────────────────────
// Formatting
// ──────────────────────────────────────────────
function formatKRW(n) {
    if (!n) return "0원";
    if (n >= 1e12) return (n / 1e12).toFixed(1) + "조";
    if (n >= 1e8) return Math.round(n / 1e8) + "억";
    if (n >= 1e4) return Math.round(n / 1e4).toLocaleString() + "만";
    return n.toLocaleString() + "원";
}

function formatAmt(n) {
    const t = Math.floor(n / 1e12);
    const b = Math.floor((n % 1e12) / 1e8);
    if (t > 0) return `${t}조 ${b > 0 ? b + '억' : ''}`;
    if (b > 0) return `${b}억`;
    return formatKRW(n);
}

// Export
if (typeof module !== 'undefined') module.exports = { RAW_DATA, computeStats, computeHeatmap, filterData, formatKRW, formatAmt, extractClient };
'''

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

// 발주공고 데이터 (랄랄라.xlsx에서 추출)
// 실제 DB 연동 시 이 파일을 API 호출로 교체

const RAW_DATA = [
    { 공고번호: "20241241380-00", 추정가격: 117430910, 지역제한: "광명/부천/시흥", 종목: "전기", 특수실적: null, 계약방법: "수의", 적격평가세부기준: null, 입력일: "2025-01-01" },
    { 공고번호: "20241241379-00", 추정가격: 197703637, 지역제한: "광명/부천/시흥", 종목: "실내건축", 특수실적: null, 계약방법: "수의", 적격평가세부기준: null, 입력일: "2025-01-01" },
    { 공고번호: "H24S115000-1/0", 추정가격: 60236000, 지역제한: "울진", 종목: "전기소방/전문소방", 특수실적: null, 계약방법: "적격심사", 적격평가세부기준: "한국수력원자력_별표-10", 입력일: "2025-01-02" },
    { 공고번호: "E052500004", 추정가격: 104750000, 지역제한: "제주", 종목: "통신", 특수실적: null, 계약방법: "적격심사", 적격평가세부기준: "한국전력공사_3억미만", 입력일: "2025-01-02" },
    { 공고번호: "2404509-01", 추정가격: 2501117000, 지역제한: "전국/전남", 종목: "통신", 특수실적: null, 계약방법: "적격심사", 적격평가세부기준: "한국토지주택공사_별표-3", 입력일: "2025-01-02" },
    { 공고번호: "E012500003", 추정가격: 295865206, 지역제한: "충남", 종목: "전기", 특수실적: "수급지점개폐기", 계약방법: "적격심사", 적격평가세부기준: "한국전력공사(배전)_3억미만", 입력일: "2025-01-02" },
    { 공고번호: "W24S151000/0", 추정가격: 91089000, 지역제한: "전국", 종목: "전기", 특수실적: "한수원등록업체", 계약방법: "적격심사", 적격평가세부기준: "한국수력원자력_별표-9", 입력일: "2025-01-02" },
    { 공고번호: "E052500001", 추정가격: 373674000, 지역제한: "전국", 종목: "기계가스설비", 특수실적: "특수실적", 계약방법: "적격심사", 적격평가세부기준: "한국전력공사_50억미만", 입력일: "2025-01-02" },
    { 공고번호: "E062500003", 추정가격: 435803000, 지역제한: "전국", 종목: "기계가스설비/건축/토건", 특수실적: "특수실적", 계약방법: "적격심사", 적격평가세부기준: "한국전력공사_50억미만", 입력일: "2025-01-02" },
    { 공고번호: "E012411447", 추정가격: 6724824031, 지역제한: "전국", 종목: "(전기,지반조성포장)/(전기,토목)/(토건,전기)", 특수실적: "지향성압입_준공길이", 계약방법: "적격심사", 적격평가세부기준: "한국전력공사(압입)_100억미만", 입력일: "2025-01-02" },
    { 공고번호: "2024-28105", 추정가격: 50318182, 지역제한: "고양", 종목: "(건축,토목)/토건/(철콘,지반조성포장,금속창호지붕,실내건축,비계구조)", 특수실적: null, 계약방법: "수의", 적격평가세부기준: null, 입력일: "2025-01-02" },
    { 공고번호: "E012500005", 추정가격: 109840000, 지역제한: "전국", 종목: "도장습식방수석공", 특수실적: "화재확산방지재", 계약방법: null, 적격평가세부기준: "한국전력공사_2억미만", 입력일: "2025-01-02" },
    { 공고번호: "E012500010", 추정가격: 31467796, 지역제한: "전국", 종목: "전기", 특수실적: "엘보분리장치", 계약방법: "수의", 적격평가세부기준: null, 입력일: "2025-01-03" },
    { 공고번호: "E012500011", 추정가격: 41315138, 지역제한: "전국", 종목: "전기", 특수실적: "엘보분리장치", 계약방법: "수의", 적격평가세부기준: null, 입력일: "2025-01-03" },
    { 공고번호: "E012500022", 추정가격: 149357785, 지역제한: "전국", 종목: "전기", 특수실적: "누전탐사장비", 계약방법: "수의", 적격평가세부기준: null, 입력일: "2025-01-03" },
    { 공고번호: "2404546-00", 추정가격: 2080207273, 지역제한: "전국/대구/경북", 종목: "전문소방", 특수실적: null, 계약방법: "적격심사", 적격평가세부기준: "한국토지주택공사_별표-3", 입력일: "2025-01-03" },
    { 공고번호: "2404547-00", 추정가격: 1615987273, 지역제한: "전국/대구/경북", 종목: "전문소방", 특수실적: null, 계약방법: "적격심사", 적격평가세부기준: "한국토지주택공사_별표-3", 입력일: "2025-01-03" },
];

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
    "광주": ["광주"],
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
                // "울산 중구" 형태 처리: 부모지역(울산) + 시군구(중구)
                const parts = fr.split(' ');
                if (parts.length >= 2 && REGION_MAP[parts[0]]) {
                    // 부모 지역이 REGION_MAP에 존재하는 경우 → 시군구 필터
                    const parentRegion = parts[0];
                    const subDistrict = parts.slice(1).join(' ');
                    // 지역제한 필드에 부모 지역이 포함되어 있어야 함
                    const parentRVals = REGION_MAP[parentRegion] || [parentRegion];
                    const parentMatched = parentRVals.some(rv => regionText.includes(rv));
                    if (!parentMatched) return false;
                    // 지역제한 필드에 시군구가 단어 단위로 포함되어 있어야 함
                    // 단순 includes가 아닌, '/' 또는 공백으로 구분된 단어로 비교
                    const regionTokens = regionText.split(/[\/\s,]+/);
                    return regionTokens.some(token => token.trim() === subDistrict);
                }
                // 광역시도 단위 또는 기존 키: 기존 방식대로 처리
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

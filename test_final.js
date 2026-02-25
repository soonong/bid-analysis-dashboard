
const { filterData, REGION_MAP } = require('./data.js');

// Mock Data
const MOCK_DATA = [
    { 공고번호: "1", 추정가격: 500000000, 지역제한: "서울/중구", 종목: "전기", 계약방법: "수의", 적격평가세부기준: "한국전력" },
    { 공고번호: "2", 추정가격: 2000000000, 지역제한: "울산/중구", 종목: "통신", 계약방법: "적격심사", 적격평가세부기준: "LH" },
    { 공고번호: "3", 추정가격: 300000000, 지역제한: "부산/중구", 종목: "전기", 계약방법: "수의", 적격평가세부기준: "기타" },
    { 공고번호: "4", 추정가격: 4000000000, 지역제한: "울산/남구", 종목: "토목", 계약방법: "적격심사", 적격평가세부기준: "한수원" },
    { 공고번호: "5", 추정가격: 5000000000, 지역제한: "전국", 종목: "건축", 계약방법: "적격심사", 적격평가세부기준: "한국전력" }
];

console.log("Running Final Verification Tests");

// Test 1: Region "울산 중구" vs "서울 중구"
{
    const filters = { regions: ["울산 중구"] };
    const res = filterData(MOCK_DATA, filters);
    const ids = res.map(r => r.공고번호).sort();
    if (JSON.stringify(ids) === JSON.stringify(["2"])) {
        console.log("[PASS] Region Filter: 울산 중구 matches only #2");
    } else {
        console.error("[FAIL] Region Filter: Expected ['2'], got", ids);
    }
}

// Test 2: Amount Range (min/max logic simulated from index.html)
{
    // index.html logic: sets minAmt/maxAmt
    const filters = { minAmt: 1000000000, maxAmt: 3000000000 }; // 10억~30억
    const res = filterData(MOCK_DATA, filters);
    const ids = res.map(r => r.공고번호).sort();
    // #2 is 20억. Matches.
    if (JSON.stringify(ids) === JSON.stringify(["2"])) {
        console.log("[PASS] Amount Filter: 10억~30억 matches #2");
    } else {
        console.error("[FAIL] Amount Filter: Expected ['2'], got", ids);
    }
}

// Test 3: Contract Method
{
    const filters = { contractMethod: "수의" };
    const res = filterData(MOCK_DATA, filters);
    const ids = res.map(r => r.공고번호).sort();
    // #1, #3 are 수의.
    if (JSON.stringify(ids) === JSON.stringify(["1", "3"])) {
        console.log("[PASS] Contract Filter: 수의 matches #1, #3");
    } else {
        console.error("[FAIL] Contract Filter: Expected ['1', '3'], got", ids);
    }
}

// Test 4: Clients (implied logic: extractClient)
{
    // data.js extractClient test
    const { extractClient } = require('./data.js');
    if (extractClient("한국전력공사_별표") === "KEPCO(한전)") {
        console.log("[PASS] Client Extraction: 한국전력 -> KEPCO(한전)");
    } else {
        console.error("[FAIL] Client Extraction");
    }

    const filters = { clients: ["KEPCO(한전)"] };
    const res = filterData(MOCK_DATA, filters);
    const ids = res.map(r => r.공고번호).sort();
    // #1 (한국전력), #5 (한국전력)
    if (JSON.stringify(ids) === JSON.stringify(["1", "5"])) {
        console.log("[PASS] Client Filter: KEPCO matches #1, #5");
    } else {
        console.error("[FAIL] Client Filter: Expected ['1', '5'], got", ids);
    }
}

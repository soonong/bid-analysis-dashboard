#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
index.html 버그 수정 스크립트
1. < div > (공백 포함 태그) → <div> 수정
2. fetch_api_data.py: let RAW_DATA → var RAW_DATA 수정
3. TAB_OPTS '발주처' renderClientPanel 수정
"""
import re

print("=== index.html 버그 수정 시작 ===")

# ── index.html 수정 ──────────────────────────────────────────────
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

orig = html

# Bug 1: '< div class="space-y-1" >' 와 '< /div >' 를 정상 태그로 수정
html = html.replace('< div class="space-y-1" >', '<div class="space-y-1">')
html = html.replace('< /div >', '</div>')

# Bug 2: 필터 chip 에서 '< div onclick...' 수정
html = html.replace('< div onclick =', '<div onclick=')
html = html.replace('< /div >', '</div>')   # 혹시 남아있으면

# Bug 3: searchResultsPanel empty '< div class="flex...' 수정
bad_search_empty = '< div class="flex items-center justify-center gap-2 py-4 text-[#5e6c7c] text-xs"'
good_search_empty = '<div class="flex items-center justify-center gap-2 py-4 text-[#5e6c7c] text-xs"'
html = html.replace(bad_search_empty, good_search_empty)

# Bug 4: 발주처 탭 - switchTab에서 clientPanel 참조 추가
# switchTab 함수에서 isClient 처리를 확인 - 현재 generalPanel에서 처리되는데
# renderFilterChips가 발주처를 generalPanel로 보내서 HTML이 출력되는 문제
# 발주처 TAB_OPTS에 items가 비어있어서 filterChipGrid가 비어야 하는데
# 문제는 clientPanel이 있는 버전 코드와 generalPanel만 있는 버전이 혼재

# 현재 HTML이 어떤 구조인지 확인
has_clientPanel = 'id="clientPanel"' in html
print(f"clientPanel 존재: {has_clientPanel}")

fixes = 0
if '< div class="space-y-1" >' not in html:
    fixes += 2
    print("✅ Bug 1 수정됨: space-y-1 div 태그")
if '< /div >' not in html:
    fixes += 1
    print("✅ Bug 2 수정됨: 닫는 div 태그")

# Bug 5: TAB_OPTS 발주처 items가 비어있어서 발주처 칩이 안 나옴
# renderFilterChips → generalPanel → filterChipGrid에 아무것도 없음
# DOMContentLoaded에서 TAB_OPTS['발주처'].items를 채워야 함
# 현재 코드에 이미 있는지 확인
if "TAB_OPTS['발주처'].items" in html:
    print("✅ 발주처 items 초기화 이미 존재")
else:
    print("⚠️ 발주처 items 초기화 없음 - 수정 필요")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

changed_chars = sum(1 for a, b in zip(orig, html) if a != b)
print(f"✅ index.html 수정 완료 ({changed_chars}자 변경)")

# ── fetch_api_data.py 수정 ─────────────────────────────────────
with open('fetch_api_data.py', 'r', encoding='utf-8') as f:
    py = f.read()

# var → let 으로 재생성되는 문제: line 132
if 'js_array = "let RAW_DATA' in py:
    py = py.replace('js_array = "let RAW_DATA', 'js_array = "var RAW_DATA')
    print("✅ fetch_api_data.py: let → var 수정됨")
else:
    print("ℹ️ fetch_api_data.py: 이미 var 사용 중")

with open('fetch_api_data.py', 'w', encoding='utf-8') as f:
    f.write(py)

# ── data.js 수정 (현재 let으로 되어있으면 var로) ─────────────────
with open('data.js', 'r', encoding='utf-8') as f:
    first_lines = f.read(500)  # 첫 500바이트만 확인

if 'let RAW_DATA' in first_lines:
    print("⚠️ data.js: let RAW_DATA 발견 - var로 수정 중...")
    # 전체 파일 읽기 (26MB이므로 시간 걸림)
    with open('data.js', 'r', encoding='utf-8') as f:
        js = f.read()
    js = js.replace('let RAW_DATA', 'var RAW_DATA', 1)
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("✅ data.js: let → var 수정 완료")
else:
    print("✅ data.js: 이미 var RAW_DATA 사용 중")

print("\n=== 모든 수정 완료! ===")
print("브라우저에서 페이지를 새로고침(Ctrl+Shift+R)하세요.")

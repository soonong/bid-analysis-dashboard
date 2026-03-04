#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
index.html 2차 버그 수정 - renderClientPanel 및 기타 공백 태그 수정
"""

print("=== index.html 2차 버그 수정 ===")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

orig_len = len(html)

# renderClientPanel 의 broken HTML tags
# '< div class="grid grid-cols-2 gap-0 p-2" >' -> '<div class="grid grid-cols-2 gap-0 p-2">'
html = html.replace('< div class="grid grid-cols-2 gap-0 p-2" >', '<div class="grid grid-cols-2 gap-0 p-2">')

# '</div >' -> '</div>'  (trailing space before >)
html = html.replace('</div >', '</div>')

# '<div onclick= "' -> '<div onclick="'  (space after onclick=)
html = html.replace('<div onclick= "', '<div onclick="')

# Also catch any '< div ... >' patterns that have spaces around the tag name
import re

# Fix < div ... > (space after <)
def fix_open_tag(m):
    return '<' + m.group(1).strip() + '>'
html = re.sub(r'< (div[^>]*?) >', fix_open_tag, html)

# Fix < /div > (space before /)
html = html.replace('< /div>', '</div>')
html = html.replace('</div >', '</div>')

# Check filterChips area for broken tags
# '< div onclick =' → '<div onclick='
html = re.sub(r'< (div|span|input|a|button)\s+onclick =', lambda m: f'<{m.group(1)} onclick=', html)

# Fix the case in renderFilterChips (line ~1455):
#   `< div onclick = "toggleChip(...)" class="filter-chip..." >`
html = re.sub(r'< div onclick = "', '<div onclick="', html)

# Count remaining broken tags
broken_open = len(re.findall(r'< [a-z]', html))
broken_close = len(re.findall(r'</ [a-z]', html))
print(f"남은 깨진 태그: open={broken_open}, close={broken_close}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ 수정 완료 (파일 {len(html) - orig_len:+d}자)")

# ── 추가: filterData 에서 dateRange 처리 확인 ──────────────────
print("\n== filterData dateRange 처리 확인 ==")
if 'dateRange' in html and 'filters.dateRange' in html:
    idx = html.find('filters.dateRange')
    line_no = html[:idx].count('\n') + 1
    print(f"dateRange 처리 at line {line_no}:")
    print(html[idx:idx+200])
else:
    print("⚠️ filterData에 dateRange 처리 없음 - 상세설정 기간필터가 그래프에 미적용됨!")
    # 이 경우 filterData를 patch해야 함

# ── filterData 에 dateRange 처리가 없으면 추가 ─────────────────
filter_data_idx = html.find('function filterData(data, filters)')
if filter_data_idx < 0:
    filter_data_idx = html.find('function filterData(')
print(f"\nfilterData at line: {html[:filter_data_idx].count(chr(10))+1 if filter_data_idx>=0 else 'NOT FOUND'}")

# dateRange 처리가 filterData 안에 있는지 확인 - 그래프 필터 연동의 핵심
daterange_in_filter = 'filters.dateRange' in html[filter_data_idx:filter_data_idx+1000] if filter_data_idx >= 0 else False
print(f"filterData 내 dateRange 처리: {daterange_in_filter}")

if not daterange_in_filter and filter_data_idx >= 0:
    print("⚠️ filterData에 dateRange 처리 추가 필요!")
    # filterData 함수의 return true 직전에 dateRange 필터 추가
    # 현재 filterData의 끝 부분을 찾아서 수정
    return_true_idx = html.find('        return true;\n    }', filter_data_idx)
    if return_true_idx > 0:
        line_no2 = html[:return_true_idx].count('\n') + 1
        print(f"  return true 위치: line {line_no2}")
        # dateRange 필터 코드 삽입
        date_filter_code = """        if (filters.dateRange && filters.dateRange.start && filters.dateRange.end) {
            const d = (row.입력일 || '').slice(0, 10);
            if (d < filters.dateRange.start || d > filters.dateRange.end) return false;
        }
"""
        html = html[:return_true_idx] + date_filter_code + html[return_true_idx:]
        print("  ✅ dateRange 필터 추가됨")
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
    else:
        print(f"  ❌ return true 위치 못 찾음 (filter_data_idx={filter_data_idx})")

print("\n=== 2차 수정 완료 ===")

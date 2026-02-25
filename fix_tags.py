
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

NEW_FUNC = """        function updateSelectedTags() {
            const allSelected = [
                ...(tempFilters.regions    || []),
                ...(tempFilters.categories || []),
                ...(tempFilters.clients    || []),
                ...(tempFilters.amtRange   || []),
                ...(tempFilters.specialOnly ? ['특수실적 있음'] : []),
            ];
            const row = document.getElementById('selectedTagsRow');
            if (!allSelected.length) {
                row.innerHTML = '<span class="text-xs text-[#5e6c7c] self-center">선택된 항목 없음</span>';
                return;
            }
            row.innerHTML = allSelected.map(function(item) {
                var esc = item.replace(/'/g, "\\\\'");
                return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium bg-primary/15 text-primary border border-primary/30">'
                    + item
                    + '<span onclick="removeSelectedTag(\\'' + esc + '\\')" class="material-symbols-outlined text-[12px] hover:text-white cursor-pointer">close</span>'
                    + '</span>';
            }).join('');
        }
"""

# Find start and end of the updateSelectedTags function (lines 1184-1207, 0-indexed: 1183-1206)
start = None
end = None
for i, line in enumerate(lines):
    if 'function updateSelectedTags()' in line and start is None:
        start = i
    if start is not None and i > start and line.strip() == '}':
        end = i
        break

if start is not None and end is not None:
    print(f"Found function at lines {start+1}-{end+1}")
    lines[start:end+1] = [NEW_FUNC]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("SUCCESS: updateSelectedTags replaced")
else:
    print(f"ERROR: function not found (start={start}, end={end})")

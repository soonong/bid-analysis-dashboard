from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # npx serve defaults to port 3000
        page.goto("http://localhost:3000/index.html")

        # 1. Check Heatmap Regions
        print("Checking Heatmap Regions...")
        page.wait_for_selector("#heatmapTable tbody tr")
        heatmap_rows = page.locator("#heatmapTable tbody tr")
        count = heatmap_rows.count()
        print(f"Heatmap rows: {count}")
        if count < 17:
            print("FAIL: Heatmap rows < 17")
        else:
            print("PASS: Heatmap rows >= 17")

        # 2. Open Filter Modal
        print("Opening Filter Modal...")
        page.get_by_role("button", name="상세설정").click()
        time.sleep(1)

        # 3. Select Region '울산' -> '중구'
        print("Selecting 울산 -> 중구...")
        # Click '울산' chip
        # The chip contains text "울산"
        # We need to be careful not to click something else.
        # Using xpath or precise text match
        page.click("xpath=//div[@id='regionChipGrid']//div[contains(@class, 'filter-chip')][.//span[text()='울산']]")
        time.sleep(0.5)
        # Select '중구' in sub panel
        page.click("xpath=//div[@id='subRegionChipGrid']//div[contains(@class, 'filter-chip')][.//span[text()='중구']]")

        # 4. Check Selected Tags in Modal
        print("Checking Selected Tags in Modal...")
        # The tag text is "울산 중구close" (because of the close icon text)
        tags_loc = page.locator("#selectedTagsRow > span")
        tags_count = tags_loc.count()
        print(f"Tags count: {tags_count}")
        found = False
        for i in range(tags_count):
            txt = tags_loc.nth(i).text_content()
            print(f"Tag {i}: {txt}")
            if "울산 중구" in txt:
                found = True

        if not found:
            print("FAIL: '울산 중구' tag not found")
        else:
            print("PASS: '울산 중구' tag found")

        # 5. Apply
        print("Applying Filters...")
        page.get_by_role("button", name="적용하기").click()
        time.sleep(1)

        # 6. Verify Dashboard Data Table
        print("Checking Data Table...")
        # Check if rows exist
        rows = page.locator("#dataTableBody tr")
        row_count = rows.count()
        print(f"Table rows: {row_count}")
        if row_count > 0:
            print("PASS: Data Table has rows")
        else:
            print("FAIL: Data Table is empty")

        # 7. Take Screenshot
        page.screenshot(path="verification_dashboard.png", full_page=True)
        print("Screenshot saved to verification_dashboard.png")

        browser.close()

if __name__ == "__main__":
    run()

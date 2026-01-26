"""
HKEX Input/Click Test
Purpose: verify Playwright can click and type in the HKEX "Stock Code / Keywords" input.
"""
import logging
import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

LANDING_URL = "https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en"
TEST_TEXT = "653"


def run() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"], slow_mo=200)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        logging.info("Opening landing page")
        page.goto(LANDING_URL, wait_until="networkidle", timeout=90000)
        page.evaluate("document.body.style.zoom='0.67'")

        logging.info("Locating search input")
        page.wait_for_selector("input#tags", state="attached", timeout=30000)

        search_input = page.get_by_role("textbox", name=re.compile(r"Stock Code", re.I))
        if search_input.count() == 0:
            search_input = page.locator('input#tags[placeholder*="Stock Code" i]').first
        if search_input.count() == 0:
            search_input = page.locator("#hkexw-equities .searchbox input#tags").first
        if search_input.count() == 0:
            search_input = page.locator("input#tags").first

        search_input.wait_for(state="visible", timeout=30000)
        search_input.scroll_into_view_if_needed(timeout=10000)
        placeholder = search_input.get_attribute("placeholder")
        logging.info(f"Search placeholder: {placeholder}")

        handle = search_input.element_handle()
        if handle:
            page.evaluate(
                "el => { el.style.outline='3px solid red'; el.style.background='#ffffcc'; }",
                handle,
            )

        box = search_input.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        else:
            search_input.click(force=True)

        page.keyboard.press("Control+A")
        page.keyboard.type(TEST_TEXT, delay=120)
        page.wait_for_timeout(500)

        actual_value = search_input.input_value()
        active_id = page.evaluate("() => document.activeElement && document.activeElement.id")
        logging.info(f"Active element id: {active_id}")
        logging.info(f"Search box contains: '{actual_value}'")
        page.screenshot(path="input_test_after_typing.png")
        logging.info("Screenshot saved: input_test_after_typing.png")

        # Click APPLY FILTERS (or press Enter if not found)
        logging.info("Clicking APPLY FILTERS")
        try:
            apply_btn = page.get_by_role("button", name=re.compile(r"Apply Filters", re.I))
            apply_btn.click()
        except Exception as e:
            logging.info(f"APPLY FILTERS not found, pressing Enter: {e}")
            search_input.press("Enter")

        page.wait_for_timeout(3000)
        page.screenshot(path="input_test_after_apply.png")
        logging.info("Screenshot saved: input_test_after_apply.png")

        # Click the stock code in the right panel table
        logging.info(f"Clicking stock code {TEST_TEXT} in the table")
        stock_link = page.locator(f'table tbody a:has-text("{TEST_TEXT}")').first
        stock_link.scroll_into_view_if_needed(timeout=10000)
        stock_link.click()

        page.wait_for_timeout(3000)
        page.screenshot(path="input_test_after_stock_click.png")
        logging.info("Screenshot saved: input_test_after_stock_click.png")

        logging.info("Pausing 5 seconds so you can see it")
        page.wait_for_timeout(5000)
        browser.close()


if __name__ == "__main__":
    try:
        run()
    except PlaywrightTimeoutError as e:
        logging.error(f"Timeout: {e}")

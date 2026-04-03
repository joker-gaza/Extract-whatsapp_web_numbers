import re
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OUTPUT_TXT = "wa_web_numbers.txt"

PHONE_REGEX = re.compile(r"(?<!\w)(\+?\d[\d\-\s\(\)]{6,20}\d)(?!\w)")
MIN_DIGITS = 8
MAX_DIGITS = 15


def normalize_phone(raw: str) -> str | None:
    if not raw:
        return None

    cleaned = re.sub(r"[^\d+]", "", raw)

    if cleaned.count("+") > 1:
        return None
    if "+" in cleaned and not cleaned.startswith("+"):
        return None

    digits = cleaned.replace("+", "")
    if not digits.isdigit():
        return None

    if not (MIN_DIGITS <= len(digits) <= MAX_DIGITS):
        return None

    return ("+" + digits) if cleaned.startswith("+") else digits


def extract_numbers(text: str) -> set[str]:
    out: set[str] = set()
    for m in PHONE_REGEX.findall(text):
        p = normalize_phone(m)
        if p:
            out.add(p)
    return out


def main():
    print("Launching Chrome and opening WhatsApp Web...")

    chrome_options = Options()

    # Keep session (so you don't scan QR every time)
    profile_dir = Path.cwd() / "chrome_profile"
    chrome_options.add_argument(f"--user-data-dir={profile_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 60)

    driver.get("https://web.whatsapp.com")

    print("If needed, scan the QR code in the Chrome window.")
    print("Waiting for WhatsApp Web to load...")

    # Wait until the chat list is present
    chat_list = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='grid']")))

    print("Loaded. Scrolling chat list to load more chats...")

    # Scroll multiple times to load more chats into DOM
    for _ in range(20):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", chat_list)
        time.sleep(0.8)

    print("Extracting numbers from the currently loaded page source...")
    numbers = extract_numbers(driver.page_source)

    print(f"Found {len(numbers)} unique numbers.")

    if numbers:
        with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
            for num in sorted(numbers):
                f.write(num + "\n")
        print(f"Saved to: {OUTPUT_TXT}")
    else:
        print("No numbers found. Try scrolling more chats manually and run again.")

    # driver.quit()


if __name__ == "__main__":
    main()
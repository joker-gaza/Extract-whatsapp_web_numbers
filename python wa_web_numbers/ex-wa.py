import re
import csv
from pathlib import Path

INPUT_FOLDER = "whatsapp_exports"
OUTPUT_CSV = "all_numbers.csv"
OUTPUT_TXT = "all_numbers.txt"

MIN_DIGITS = 8
MAX_DIGITS = 15

PHONE_PATTERN = re.compile(r"(?<!\w)(\+?\d[\d\-\s\(\)]{6,20}\d)(?!\w)")


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
    for m in PHONE_PATTERN.findall(text):
        p = normalize_phone(m)
        if p:
            out.add(p)
    return out


def read_text_best_effort(p: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "cp1256", "latin-1"):
        try:
            return p.read_text(encoding=enc)
        except UnicodeDecodeError:
            pass
    return p.read_text(encoding="latin-1", errors="ignore")


def main():
    folder = Path(INPUT_FOLDER)
    if not folder.exists():
        raise FileNotFoundError(f"Folder '{INPUT_FOLDER}' not found.")

    txt_files = sorted(folder.rglob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in '{INPUT_FOLDER}'.")

    rows = []
    all_numbers: set[str] = set()

    for f in txt_files:
        content = read_text_best_effort(f)
        nums = extract_numbers(content)
        for n in nums:
            all_numbers.add(n)
            rows.append({"phone": n, "source_file": f.name})

    unique_sorted = sorted(all_numbers)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as out:
        for n in unique_sorted:
            out.write(n + "\n")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as out:
        w = csv.DictWriter(out, fieldnames=["phone", "source_file"])
        w.writeheader()
        # optional: keep duplicates across files (shows where it came from)
        w.writerows(sorted(rows, key=lambda x: (x["phone"], x["source_file"])))

    print(f"Chats scanned: {len(txt_files)}")
    print(f"Unique numbers: {len(unique_sorted)}")
    print(f"Saved: {OUTPUT_TXT}")
    print(f"Saved: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
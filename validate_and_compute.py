import csv
import sys
from pathlib import Path

DATA_PATH = Path("data") / "students.csv"
OUTPUT_PATH = Path("average_age.txt")


def parse_and_validate_students(path: Path) -> list[int]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        expected = ["id", "name", "age"]
        if reader.fieldnames != expected:
            raise ValueError(f"Expected header {expected}, got {reader.fieldnames}")

        ages: list[int] = []
        for row_num, row in enumerate(reader, start=2):  # header is line 1
            age_str = (row.get("age") or "").strip()

            # Reject anything that isn't digits only
            if not age_str.isdigit():
                raise ValueError(f"Row {row_num}: age must be a non-negative integer, got {age_str!r}")

            ages.append(int(age_str))

        if not ages:
            raise ValueError("No data rows found in students.csv")

        return ages


def write_average(avg: float, path: Path) -> None:
    path.write_text(f"Average age: {avg:.2f}\n", encoding="utf-8")


def main() -> int:
    ages = parse_and_validate_students(DATA_PATH)
    avg = sum(ages) / len(ages)
    write_average(avg, OUTPUT_PATH)
    print(f"OK: wrote {OUTPUT_PATH} (n={len(ages)}, avg={avg:.2f})")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        # Critical: non-zero exit code so Actions FAILS and does not proceed
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)

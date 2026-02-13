import csv
import sys
from pathlib import Path


DATA_PATH = Path("data") / "students.csv"
OUTPUT_PATH = Path("average_age.txt")


def validate_csv(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist.")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV file is empty.")

    header = rows[0]
    expected_header = ["id", "name", "age"]

    if header != expected_header:
        raise ValueError(
            f"Expected header {expected_header}, but got {header}"
        )

    ages = []

    for i, row in enumerate(rows[1:], start=2):  # start=2 for line numbers
        if len(row) != 3:
            raise ValueError(f"Row {i} does not have exactly 3 columns: {row}")

        age_str = row[2]

        if not age_str.isdigit():
            raise ValueError(f"Row {i}: age must be a non-negative integer, got {age_str!r}")

        age = int(age_str)

        if age < 0:
            raise ValueError(f"Row {i}: age cannot be negative, got {age}")

        ages.append(age)

    if not ages:
        raise ValueError("No student rows found.")

    return ages


def compute_average(ages):
    return sum(ages) / len(ages)


def write_output(avg, path: Path):
    with path.open("w", encoding="utf-8") as f:
        f.write(f"Average age: {avg:.2f}\n")


def main():
    try:
        ages = validate_csv(DATA_PATH)
        avg = compute_average(ages)
        write_output(avg, OUTPUT_PATH)
        print("Validation passed. Average age computed and written successfully.")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)  # This makes GitHub Actions fail the job


if __name__ == "__main__":
    main()

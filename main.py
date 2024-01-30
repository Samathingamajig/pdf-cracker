import fitz
import sys
from multiprocessing import Pool


def find_password_range(args: tuple[str, str]) -> (str, bool):
    pdf_path, min_val, max_val = args
    doc = fitz.open(pdf_path)
    try:
        # Try opening the PDF with the provided password
        for i in range(min_val, max_val):
            password = f"{i:>04}"
            res = doc.authenticate(password)
            successful = res != 0
            if successful:
                return password, True
        return password, False
    except Exception as e:
        # Handle other exceptions such as file not found or not a PDF
        print(f"An error occurred: {e}")
        return password, False


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} [PATH]")
        return 1

    pdf_path = sys.argv[1]

    try:
        doc = fitz.open(pdf_path)
    except fitz.FileNotFoundError:
        print(f"Could not find file: {pdf_path}")
        return 1
    except Exception as e:
        print(f"An exception occurred: {e}")
        return 1

    if not doc.needs_pass:
        print(f"{pdf_path} is not protected by a password, or is invalid")
        return 1

    doc.close()

    cracked_password = ""

    with Pool() as pool:
        results = pool.map(
            find_password_range,
            [(pdf_path, i, i + 500) for i in range(0, 10_000, 500)],
        )

        for password, cracked in results:
            if cracked:
                cracked_password = password

        if len(cracked_password) == 0:
            print(f"{pdf_path}'s password was not 0000-9999")
            return 1

    print(f"{pdf_path}: {cracked_password}")


if __name__ == "__main__":
    raise SystemExit(main())

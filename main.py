import pikepdf
import sys
import io
from multiprocessing import Pool


def read_pdf(pdf_path: str) -> (io.BytesIO, IOError):
    try:
        with open(pdf_path, "rb") as f:
            return io.BytesIO(f.read()), None
    except IOError as e:
        return None, e


def has_password(bin_pdf: io.BytesIO) -> bool:
    try:
        # Try opening the PDF without a password
        with pikepdf.open(bin_pdf):
            return False
    except pikepdf.PasswordError:
        # Raised if the password is incorrect
        return True
    except Exception as e:
        # Handle other exceptions such as file not found or not a PDF
        print(f"An error occurred: {e}")
        return False


def is_password_correct(args):
    bin_pdf, password = args
    try:
        # Try opening the PDF with the provided password
        with pikepdf.open(bin_pdf, password=password):
            return password, True
    except pikepdf.PasswordError:
        # Raised if the password is incorrect
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

    bin_pdf, err = read_pdf(pdf_path)
    if err is not None:
        print(f"Error opening {pdf_path}: {err}")
        return 1

    if not has_password(bin_pdf):
        print(f"{pdf_path} is not protected by a password, or is invalid")
        return 1

    cracked_password = ""

    passwords = (f"{i:>04}" for i in range(10_000))

    with Pool() as pool:
        results = pool.map(
            is_password_correct, [(bin_pdf, password) for password in passwords]
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

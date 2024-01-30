import fitz
import sys

pdf_path = sys.argv[1]
with fitz.open(pdf_path) as doc:
    for i in range(10_000):
        if doc.authenticate(f"{i:<04}") != 0:
            print(f"{i:<04}")

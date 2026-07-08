import fitz
import sys

pdf_path = sys.argv[1]
pdf = fitz.open(pdf_path)
print(len(pdf))
pdf.close()

import fitz, sys, os

pdf_path = sys.argv[1]
out_dir = sys.argv[2]
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
for i in range(len(doc)):
    text = doc[i].get_text()
    with open(os.path.join(out_dir, f"page_{i+1:03d}.txt"), "w", encoding="utf-8") as f:
        f.write(text)
doc.close()
print(f"Extracted {len(doc)} pages to {out_dir}")

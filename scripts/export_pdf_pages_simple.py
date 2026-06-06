import fitz, sys, os

pdf_path = sys.argv[1]
out_dir = sys.argv[2]
pages = sys.argv[3:]  # format: page:name.png
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
for p in pages:
    page_num, name = p.split(":")
    page = doc[int(page_num)-1]
    pix = page.get_pixmap(dpi=200)
    pix.save(os.path.join(out_dir, name))
    print(f"Saved {name}")
doc.close()

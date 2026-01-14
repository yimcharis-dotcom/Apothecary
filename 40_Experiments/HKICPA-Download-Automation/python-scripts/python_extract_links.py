from pypdf import PdfReader

pdf_path = "contentpage.pdf"
reader = PdfReader(pdf_path)

urls = []
for page in reader.pages:
    annots = page.get("/Annots") or []
    for a in annots:
        obj = a.get_object()
        action = obj.get("/A") or {}
        uri = action.get("/URI")
        if isinstance(uri, str) and uri.startswith(("http://", "https://")):
            urls.append(uri)

seen = set()
unique_urls = []
for u in urls:
    if u not in seen:
        seen.add(u)
        unique_urls.append(u)

with open("hkicpa_links.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(unique_urls))

print(f"✓ Extracted {len(unique_urls)} unique URLs to hkicpa_links.txt")

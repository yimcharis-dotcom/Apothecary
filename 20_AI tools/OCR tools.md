---
created: 2026-01-20
Tags:
  - tools
  - OCR
  - guides
  - tesseract
  - pytesseract
  - OCRmyPDF
---
# Tesseract   #tesseract 
GitHub: [GitHub - Tesseract (main repository)](https://github.com/tesseract-ocr/tesseract)  
Tesseract User Manual: [Tesseract User Manual](https://github.com/tesseract-ocr/tessdoc)
---
## 1. Python's built-in help system
Use Python’s help to explore what’s available: #help
```python
# In Python, import the library first

Import pytesseract
Import ocrmypdf

# Then get help

Help (pytesseract)
Help (ocrmypdf)

# Or get help on specific functions

Help (pytesseract. Image_to_string)
Help (ocrmypdf. Ocr)
```
---
 Using dir () to see what's available
```python
import pytesseract
import ocrmypdf

# See all available functions/attributes
print(dir(pytesseract))
print(dir(ocrmypdf))

# Filter to see only functions (not private/internal stuff)
print([x for x in dir (pytesseract) if not x.startswith ('_')])
```
---
## 2. Quick reference in Python
See function signatures:
```python
import pytesseract
import ocrmypdf
import inspect

# See what parameters a function accepts
print(inspect.signature(pytesseract.image_to_string))
print(inspect.signature(ocrmypdf.ocr))

# Get full docstring
print(pytesseract.image_to_string.__doc__)
print(ocrmypdf.ocr.__doc__)
```
---
# pytesseract: #pytesseract 
GitHub: https://github.com/madmaze/pytesseract  
PyPI: https://pypi.org/project/pytesseract/  
Read the Docs: https://pytesseract.readthedocs.io/  
---
## pytesseract main functions:
``` python
pytesseract.image_to_string()      # Extract text
pytesseract.image_to_string(image)
pytesseract.image_to_data()         # Get detailed data
pytesseract.image_to_boxes()         # Get bounding boxes
pytesseract.image_to_pdf_or_hocr()  # Convert to PDF/HOCR
```
---
Pattern for image OCR:
```python
import pytesseract
from PIL import Image

image = Image.open('file.png')
text = pytesseract.image_to_string(image)
```
---
**Extract text from a scanned image**
```python
import pytesseract
from PIL import Image

# Your image
img = Image.open('scanned_page.png')

# Extract text
text = pytesseract.image_to_string(img, lang='eng')
print(text)

# Save to file
with open('extracted_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)
```
```python
## Extract text from imagen
import pytesseract
from PIL import Image

img = Image.open('image.png')
text = pytesseract.image_to_string(img, lang='eng')

```
---
Multiple images
```python
import pytesseract
from PIL import Image
import os

# Process all images in a folder
image_folder = 'images/'
for filename in os.listdir(image_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        img = Image.open(os.path.join(image_folder, filename))
        text = pytesseract.image_to_string(img, lang='eng')
        
        # Save extracted text
        output_file = f'extracted_{filename}.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Processed {filename}")
```
---
# ocrmypdf: #OCRmyPDF 
Official docs: https://ocrmypdf.readthedocs.io/  
GitHub: https://github.com/ocrmypdf/OCRmyPDF   
 PyPI: https://pypi.org/project/ocrmypdf/  
---
Help for OCRmyPDF
```python
## . Command-line help
For ocrmypdf (since it's also a CLI tool):

# In PowerShell
ocrmypdf --help
### ocrmypdf main functions:
# See all options
ocrmypdf --help-verbose
```
---
Pattern for PDF OCR:
```python
import ocrmypdf

# Basic OCR on a PDF
ocrmypdf.ocr('input.pdf', 'output.pdf')

# With options
ocrmypdf.ocr(
    'scanned_document.pdf',
    'searchable_document.pdf',
    language='eng',  # or 'chi_sim' for Chinese
    deskew=True,     # Fix skewed pages
    clean=True       # Clean up images
)
```
```python
ocrmypdf.ocr()                      # Main OCR function
ocrmypdf.ocr()                      # (that's the main one!)
ocrmypdf.ocr('input.pdf', 'output.pdf')
```
---
Programmatic usage:
```python
import ocrmypdf

# OCR a PDF file
try:
    ocrmypdf.ocr('input.pdf', 'output.pdf', language='eng')
    print("OCR completed successfully!")
except ocrmypdf.exceptions.PriorOcrFoundError:
    print("PDF already has text layer")
except Exception as e:
    print(f"Error: {e}")
```
---

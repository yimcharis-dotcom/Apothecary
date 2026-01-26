@echo off
set /p IMAGE_PATH="Enter image path: "
set /p LANG="Language (eng/chi_sim): "
"C:\PROGRA~1\Tesseract-OCR\tesseract.exe" "%IMAGE_PATH%" stdout -l %LANG%
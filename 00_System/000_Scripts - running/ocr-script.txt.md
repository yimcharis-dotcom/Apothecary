```
Async function ocr (tp) {
    // Prompt for image path
    Const imagePath = await tp.System.Prompt ("Enter image path");
    If (! ImagePath) return "❌ No image path provided";
    
    // Prompt for language
    const lang = await tp.system.prompt("Language (eng/chi_sim)", "eng");
    if (!lang) return "❌ No language provided";
    
    // Run Tesseract
    const command = `"C:\\PROGRA~1\\Tesseract-OCR\\tesseract.exe" "${imagePath}" stdout -l ${lang}`;
    const result = await tp.system.execCommand(command);
    
    return result;
}

Module. Exports = ocr;

```
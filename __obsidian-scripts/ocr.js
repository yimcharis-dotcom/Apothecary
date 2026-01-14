async function ocr(tp) {
    // Prompt for image path
    const imagePath = await tp.system.prompt("Enter image path");
    if (!imagePath) return "❌ No image path provided";
    
    // Prompt for language
    const lang = await tp.system.prompt("Language (eng/chi_sim)", "eng");
    if (!lang) return "❌ No language provided";
    
    // Run Tesseract
    const command = `"C:\\PROGRA~1\\Tesseract-OCR\\tesseract.exe" "${imagePath}" stdout -l ${lang}`;
    const result = await tp.system.execCommand(command);
    
    return result;
}

module.exports = ocr;

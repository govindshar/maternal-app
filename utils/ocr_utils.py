from PIL import Image
import pytesseract

def extract_text_from_image(image_file):
    try:
        image = Image.open(image_file).convert("RGB")
        text = pytesseract.image_to_string(image)
        return text.strip() or "❌ Could not read text clearly."
    except Exception as e:
        return f"❌ OCR Error: {str(e)}"

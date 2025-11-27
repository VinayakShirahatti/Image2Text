import os
import io
from PIL import Image
import numpy as np
import cv2
import pytesseract

pytesseract_path = r"C:\Users\Vinayak Shirahatti\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = pytesseract_path

if not os.path.exists(pytesseract_path):
    raise FileNotFoundError(f"Tesseract not found at {pytesseract_path}.")

def preprocess_image(img_pil: Image.Image) -> Image.Image:
    """Convert to grayscale, resize, and apply adaptive threshold for OCR."""
    img_cv = cv2.cvtColor(np.array(img_pil.convert("RGB")), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Resize
    h, w = gray.shape[:2]
    gray = cv2.resize(gray, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
    
    # Adaptive threshold
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 31, 15)
    return Image.fromarray(th)

def run_ocr(pil_img: Image.Image) -> dict:
    """Run pytesseract and return OCR text."""
    pre = preprocess_image(pil_img)
    
    try:
        text = pytesseract.image_to_string(pre)
    except Exception as e:
        raise RuntimeError(f"pytesseract failed: {e}")
    
    return {"ocr_text": text.strip()}
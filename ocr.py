import pytesseract
import cv2
import numpy as np
from PIL import Image


# ---------------------------------------------------
# TESSERACT PATH
# ---------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ---------------------------------------------------
# OCR FUNCTION
# ---------------------------------------------------

def extract_text(image):

    # Convert PIL image to OpenCV image
    image = np.array(image)

    # Convert RGB to BGR
    image = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2BGR
    )

    # ------------------------------------------------
    # 1. GRAYSCALE
    # ------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # ------------------------------------------------
    # 2. UPSCALE IMAGE
    # ------------------------------------------------

    scale = 4

    resized = cv2.resize(
        gray,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )

    # ------------------------------------------------
    # 3. NOISE REMOVAL
    # ------------------------------------------------

    denoised = cv2.GaussianBlur(
        resized,
        (3, 3),
        0
    )

    # ------------------------------------------------
    # 4. THRESHOLD
    # ------------------------------------------------

    threshold = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    # ------------------------------------------------
    # 5. OCR
    # ------------------------------------------------

    config = r"--oem 3 --psm 6"

    text = pytesseract.image_to_string(
        threshold,
        config=config
    )

    return text
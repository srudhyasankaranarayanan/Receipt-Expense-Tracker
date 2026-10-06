import cv2
import easyocr
import numpy as np
from PIL import Image


# --------------------------------------------------
# CREATE OCR READER
# --------------------------------------------------

reader = None


def get_reader():
    global reader

    if reader is None:
        reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    return reader


# --------------------------------------------------
# IMAGE PREPROCESSING
# --------------------------------------------------

def preprocess_image(image):

    # Convert PIL image to NumPy
    img = np.array(image)

    # RGB → BGR
    img = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2BGR
    )

    # Convert to grayscale
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # Upscale image
    gray = cv2.resize(
        gray,
        None,
        fx=1.5,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    # Remove noise
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Improve contrast
    gray = cv2.equalizeHist(gray)

    return gray


# --------------------------------------------------
# OCR WITH POSITION INFORMATION
# --------------------------------------------------

def extract_text_with_boxes(image):

    processed = preprocess_image(image)

    results = get_reader().readtext(
        processed,
        detail=1,
        paragraph=False,
        width_ths=0.7,
        height_ths=0.7
    )

    detected = []

    for result in results:

        box = result[0]
        text = result[1]
        confidence = result[2]

        if confidence < 0.20:
            continue

        # Find center position
        xs = [point[0] for point in box]
        ys = [point[1] for point in box]

        center_x = sum(xs) / len(xs)
        center_y = sum(ys) / len(ys)

        detected.append({
            "text": text.strip(),
            "confidence": confidence,
            "x": center_x,
            "y": center_y
        })

    return detected


# --------------------------------------------------
# GROUP OCR RESULTS INTO ROWS
# --------------------------------------------------

def group_into_rows(detected):

    detected = sorted(
        detected,
        key=lambda item: item["y"]
    )

    rows = []

    for item in detected:

        placed = False

        for row in rows:

            # Compare Y positions
            if abs(
                item["y"] - row["avg_y"]
            ) < 35:

                row["items"].append(item)

                # Update average Y
                row["avg_y"] = sum(
                    x["y"]
                    for x in row["items"]
                ) / len(row["items"])

                placed = True

                break

        if not placed:

            rows.append({
                "avg_y": item["y"],
                "items": [item]
            })

    # Sort each row from left → right
    for row in rows:

        row["items"] = sorted(
            row["items"],
            key=lambda x: x["x"]
        )

    return rows


# --------------------------------------------------
# RETURN ORGANIZED OCR TEXT
# --------------------------------------------------

def extract_text(image):

    detected = extract_text_with_boxes(image)

    rows = group_into_rows(detected)

    output = []

    for row in rows:

        line = " ".join(
            item["text"]
            for item in row["items"]
        )

        output.append(line)

    return "\n".join(output)
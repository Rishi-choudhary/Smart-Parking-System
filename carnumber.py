import cv2
import numpy as np
import pytesseract

# Load tesseract library
pytesseract.pytesseract.tesseract_cmd = r"D:/Tesseract-OCR/tesseract.exe" # Path to your tesseract.exe



def number_plate_detection(image):
    # Convert to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection
    edged = cv2.Canny(blur, 100, 200)

    # Find contours in the edged image
    contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # For each contour, approximate the shape and detect if it's a rectangle
    number_plates = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        if len(approx) == 4:
            number_plates.append(approx)

    # If any number plates were found, draw them on the original image
    if number_plates:
        for plate in number_plates:
            cv2.drawContours(image, [plate], -1, (0, 255, 0), 2)

    return image

def ocr(image):
    # Apply OCR on the cropped number plate image
    text = pytesseract.image_to_string(image)
    print(text)
    return text

ocr("Karnataka_India_registration_plate_KA_19_EQ_1316.jpg")

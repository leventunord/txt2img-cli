import subprocess
from datetime import datetime
import pytesseract
import cv2
import numpy as np

def scan():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scan_filename = f"scan_{timestamp}.png"
    drawing_filename = f"drawing_{timestamp}.png"

    cmd = [
        "scanimage",
        "--device-name=fujitsu:fi-6125dj:140948",
        "--format=png",
        "--source=ADF Duplex",
        "--mode=Gray",
        "--resolution=300",
        "--page-width=105",
        "--page-height=140",
        f"--batch=./tmp/temp_%d.png",
        "--batch-start=1",
        "--batch-count=2"
    ]

    scan = subprocess.run(cmd, capture_output=True, text=True)
    # print(scan.stderr)

    if scan.returncode != 0:
        print("Scan Failed.")
        exit(1)

    corrected_img, drawing = parse_scanned()
    cv2.imwrite(f"./imgs/{scan_filename}", corrected_img)
    cv2.imwrite(f"./imgs/{drawing_filename}", drawing)

    return drawing_filename
    
def parse_scanned():
    img = is_darker("./tmp/temp_1.png", "./tmp/temp_2.png")

    corrected_img, gen_loc, angle = correct_orientation(img)

    if angle == -1:
        raise RuntimeError("Cannot find 'generating'")

    drawing = crop_drawing_area(corrected_img, gen_loc)
    return corrected_img, drawing

def is_darker(image_path1, image_path2):
    img1 = cv2.imread(image_path1, 0)
    img2 = cv2.imread(image_path2, 0)

    sum1 = np.sum(img1)
    sum2 = np.sum(img2)

    if sum1 < sum2:
        return img1
    else:
        return img2
        
def find_generating_line(img):
    """
    OCR Helper
    """
    custom_config = r'--oem 3 --psm 6'
    d = pytesseract.image_to_data(img, config=custom_config, output_type=pytesseract.Output.DICT, lang='eng')

    for i, text in enumerate(d["text"]):
        if "generating" in text.lower():
            x, y, w, h = d["left"][i], d["top"][i], d["width"][i], d["height"][i]
            return (x, y, w, h)

    return None

def correct_orientation(img):
    loc = find_generating_line(img)
    if loc:
        return img, loc, 0  # correct
    else:
        # try rotate 180 degrees
        rotated = cv2.rotate(img, cv2.ROTATE_180)
        loc2 = find_generating_line(rotated)
        if loc2:
            return rotated, loc2, 180
        else:
            return img, None, -1  # no generating line

def crop_drawing_area(img, loc):
    x, y, w, h = loc
    height, width = img.shape

    draw_y_start = y + 3 * h
    draw_y_end = height - w
    draw_x_start = x
    draw_x_end = width - x

    cropped = img[draw_y_start:draw_y_end, draw_x_start:draw_x_end]
    return cropped
import subprocess
from datetime import datetime
import pytesseract
import cv2

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

    corrected_img, drawing = get_imgs()
    cv2.imwrite(f"./imgs/{scan_filename}", corrected_img)
    cv2.imwrite(f"./imgs/{drawing_filename}", drawing)

    return None
    
def get_imgs():
    img_1 = cv2.imread("./tmp/temp_1.png", 0) # read in gray
    img_2 = cv2.imread("./tmp/temp_2.png", 0) # read in gray

    corrected_img, gen_loc, angle = correct_orientation(img_1)
    if angle == -1:
        corrected_img, gen_loc, angle = correct_orientation(img_2)

    drawing = crop_drawing_area(corrected_img, gen_loc)
    return corrected_img, drawing
        


def find_generating_line(img):
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    for i, text in enumerate(d["text"]):
        if "generating" in text:
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
    height = img.shape[0]
    draw_y_start = y + h + 10  # add space
    draw_crop = img[draw_y_start:height, :]
    return draw_crop
import cv2
import numpy as np
from pathlib import Path

IMG_DIR = Path("static/img/talk-content")
OUTPUT_SIZE = 512
CROP_SCALE = 3.0
HAIR_EXTEND = 0.3  # hair extends ~30% of face height above detected face box
MIN_HEAD_MARGIN = 0.05  # 5% of crop above estimated top of hair

cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

for img_path in sorted(IMG_DIR.iterdir()):
    if img_path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        continue

    img = cv2.imread(str(img_path))
    if img is None:
        print(f"SKIP (unreadable): {img_path.name}")
        continue

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        faces = cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(20, 20))

    if len(faces) > 0:
        fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])
        face_cx = fx + fw // 2
        head_top = int(fy - HAIR_EXTEND * fh)

        crop_side = int(max(fw, fh) * CROP_SCALE)
        crop_side = min(crop_side, min(w, h))

        # place crop so there's MIN_HEAD_MARGIN above the hair
        margin_px = int(crop_side * MIN_HEAD_MARGIN)
        top = head_top - margin_px
        left = face_cx - crop_side // 2

        top = max(0, min(top, h - crop_side))
        left = max(0, min(left, w - crop_side))

        cropped = img[top:top + crop_side, left:left + crop_side]
        status = "face"
    else:
        side = min(w, h)
        top = (h - side) // 2
        left = (w - side) // 2
        cropped = img[top:top + side, left:left + side]
        status = "CENTER (no face)"

    resized = cv2.resize(cropped, (OUTPUT_SIZE, OUTPUT_SIZE), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(img_path), resized)
    print(f"{status:>20s}: {img_path.name}")

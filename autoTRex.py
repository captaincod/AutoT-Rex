import numpy as np
import pyautogui as pyautogui
import mss
import mss.tools
import time
from skimage.filters import threshold_li
import cv2
from skimage.measure import regionprops, label


def has_vline(region):
    lines = np.sum(region.image, 0) // region.image.shape[0]
    return 1 in lines


for i in range(5):
    print(f"{5 - i} сек до начала, приготовьте браузер")
    time.sleep(1)

with mss.mss() as sct:
    # monitor = {"top": 300, "left": 570, "width": 760, "height": 150}
    monitor = {"top": 300, "left": 660, "width": 160, "height": 150}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
    sct_img = sct.grab(monitor)
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)

    key = cv2.waitKey(1)
    while True:
        if key == ord('q'):
            break

        sct_img = np.array(sct.grab(monitor))
        gray = np.mean(sct_img, 2).astype("uint8")
        threshold = threshold_li(gray)
        binary = (gray < threshold).astype(int)
        labeled = label(binary)
        regions = regionprops(labeled)
        for region in regions:
            if region.image.shape[0] < 23:
                labeled[np.where(labeled == region.label)] = 0
        for region in regions:
            if has_vline(region):
                pyautogui.keyDown("space")

"""
mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
print(output)
"""

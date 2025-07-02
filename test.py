import cv2
import numpy as np
import requests

map = cv2.imread("img/map.png")
toge = cv2.imread("img/user_avatar/liquan.png", cv2.IMREAD_UNCHANGED)

print(type(map))

fh, fw = toge.shape[:2]
# 20, 120, 300, ..., 1650   => intv = 170
# 990, .., 140  => intv = 106.25 = 106
x, y = 1650, 140+106*6

roi = map[y:(y+fh), x:(x+fw)]

if toge.shape[-1] == 4:
    f_rgb = toge[:, :, :3]
    alpha = toge[:, :, 3] / 255.0
else:
    f_rgb = toge
    alpha = np.ones((fh, fw), dtype=np.float32)

roi = roi.astype(float)
f_rgb = f_rgb.astype(float)
alpha_inv = 1.0 - alpha

foreground_part = alpha[:, :, np.newaxis] * f_rgb
background_part = alpha_inv[:, :, np.newaxis] * roi

blended = cv2.add(foreground_part, background_part)

map[y:(y+fh), x:(x+fw)] = blended.astype(np.uint8)

cv2.imwrite("img/newmaptest.png", map)

cv2.imshow("", map)
cv2.waitKey(0)
cv2.destroyAllWindows()
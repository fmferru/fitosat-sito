import cv2, numpy as np, sys
src, dst, top = sys.argv[1], sys.argv[2], float(sys.argv[3])   # top: frazione dove inizia il suolo
im = cv2.imread(src)
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
loc = cv2.GaussianBlur(g, (0, 0), 12)
H = im.shape[0]
mask = ((g < loc * 0.55) & (np.arange(H)[:, None] > int(H * (top + 0.04)))).astype(np.uint8) * 255
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
out = cv2.inpaint(im, mask, 6, cv2.INPAINT_TELEA)
cv2.imwrite(dst, out); print('masked px', int((mask > 0).sum()))

import sys, cv2, numpy as np
U = sys.argv[1]
def fix(src, dst, spots):
    img = cv2.imread(src)
    mask = np.zeros(img.shape[:2], np.uint8)
    for x, y, r in spots: cv2.circle(mask, (x, y), r, 255, -1)
    out = cv2.inpaint(img, mask, 6, cv2.INPAINT_TELEA)
    cv2.imwrite(dst, out, [cv2.IMWRITE_JPEG_QUALITY, 95])
    return out
a = fix(U + '/997736bc-image.jpg', 'atardecer.jpg', [(1189, 606, 10)])
b = fix(U + '/df970929-image.jpg', 'lado_a_lado.jpg', [(555, 482, 7)])
cv2.imwrite('z5b.png', cv2.resize(a[530:680, 1100:1280], (540, 450)))
cv2.imwrite('z2b.png', cv2.resize(b[440:530, 500:620], (480, 360)))

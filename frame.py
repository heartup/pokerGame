import cv2
import os
import numpy as np

class Person_RECT:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

STD_WIDTH = 494
STD_HEIGHT = 386

BKG_THRESH = 120

person = {'l': Person_RECT(14, 14, 494, 386),
          'r': Person_RECT(1411, 14, 494, 386),
          'b': Person_RECT(628, 447, 661, 523)}

card_width = 85
card_height = 118

gap_x = 101
gap_y = 131

card3_1_x = 4
card3_1_y = 265


frame = 0

os.mkdir('/Users/lhh/card/video/{:d}'.format(frame))
img = cv2.imread('/Users/lhh/card/video/a.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
img_w, img_h = np.shape(img)[:2]
bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
thresh_level = bkg_level + BKG_THRESH
ret, thresh = cv2.threshold(blur, thresh_level, 255, cv2.THRESH_BINARY_INV)

for p_name, rect in person.items():
    imgCrop = thresh[rect.y:rect.y + rect.height, rect.x:rect.x + rect.width]
    if rect.width != STD_WIDTH:
        imgCrop = cv2.resize(imgCrop, (STD_WIDTH, STD_HEIGHT))

    cv2.imwrite('/Users/lhh/card/video/{:d}/'.format(frame) + p_name + '.png', imgCrop)

    for i in range(3):
        y = card3_1_y - i * gap_y
        for j in range(5):
            x = card3_1_x + j * gap_x
            card = imgCrop[y:y+card_height, x:x+card_width]
            cv2.imwrite('/Users/lhh/card/video/{:d}/'.format(frame) + p_name + '_{:d}{:d}.png'.format(i, j), card)
            card_clr = card[3:43, 3:37]
            card_clr[36:43, 27:37] = 0
            cv2.imwrite('/Users/lhh/card/video/{:d}/'.format(frame) + p_name + '_card_{:d}{:d}_clr.png'.format(i, j), card_clr)
            card_num = card[39:114, 30:82]
            cv2.imwrite('/Users/lhh/card/video/{:d}/'.format(frame) + p_name + '_card_{:d}{:d}_num.png'.format(i, j), card_num)


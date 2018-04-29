import cv2
import os

# img = cv2.imread("/Users/lhh/Desktop/logo.png")
stream = cv2.VideoCapture('/Users/lhh/card/video/20180426231735.mp4')

person = {'l':14, 'r':1411}

# imgCrop = img[14:14+386, 14:14+494]


card_width = 85
card_height = 118

gap_x = 101
gap_y = 131

card3_1_x = 4
card3_1_y = 265


frame = 0
quit = 0  # Loop control variable
while quit == 0:
    os.mkdir('/Users/lhh/card/video/{:d}'.format(frame))
    img = stream.read()[1]
    cv2.imwrite('/Users/lhh/card/video/{:d}/frame.png'.format(frame), img)

    for p_name,x_pos in person.items():
        imgCrop = img[14:14 + 386, x_pos:x_pos + 494]
        cv2.imwrite('/Users/lhh/card/video/{:d}/'.format(frame) + p_name + '.png', imgCrop)

        for i in range(3):
            y = card3_1_y - i * gap_y
            for j in range(5):
                x = card3_1_x + j * gap_x
                card = imgCrop[y:y+card_height, x:x+card_width]
                cv2.imwrite('/Users/lhh/card/video/{:d}/'.format(frame) + p_name + '_{:d}{:d}.png'.format(i, j), card)
                card_clr = card[3:43, 3:37]
                cv2.imwrite('/Users/lhh/card/video/{:d}/'.format(frame) + p_name + '_card_{:d}{:d}_clr.png'.format(i, j), card_clr)
                card_num = card[39:114, 30:82]
                cv2.imwrite('/Users/lhh/card/video/{:d}/'.format(frame) + p_name + '_card_{:d}{:d}_num.png'.format(i, j), card_num)

    frame += 1

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1

# card1 = imgCrop[265:265+118,4:4+85]
# cv2.imwrite('/Users/lhh/card/video/card1.png', card1)

# Display cropped image
# cv2.imshow("Image", img)
# cv2.imshow("Crop", imCrop)
# cv2.waitKey(0)

# cv2.namedWindow("Image")
# cv2.selectROI("Image", img[1])
# cv2.imshow("Image", img[1])
# cv2.waitKey(0)
# cv2.destroyAllWindows()
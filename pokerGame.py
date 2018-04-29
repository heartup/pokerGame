import cv2
import numpy as np
import time
import os
import match
import video

### ---- INITIALIZATION ---- ###
# Define constants and initialize variables

## Camera settings
IM_WIDTH = 1920
IM_HEIGHT = 1080
FRAME_RATE = 10

CLR_DIFF_MAX = 2000
NUM_DIFF_MAX = 700

## Initialize calculated frame rate because it's calculated AFTER the first time it's displayed
frame_rate_calc = 1
freq = cv2.getTickFrequency()

## Define font to use
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize camera object and video feed from the camera. The video stream is set up
# as a seperate thread that constantly grabs frames from the camera feed.
# See VideoStream.py for VideoStream class definition
## IF USING USB CAMERA INSTEAD OF PICAMERA,
## CHANGE THE THIRD ARGUMENT FROM 1 TO 2 IN THE FOLLOWING LINE:
videostream = video.VideoStream((IM_WIDTH, IM_HEIGHT), FRAME_RATE,
                                      '/Users/lhh/card/video/20180426231735.mp4').start()
time.sleep(1)  # Give the camera time to warm up

# Load the train rank and suit images
path = os.path.dirname(os.path.abspath(__file__))
train_clrs = match.load_clrs(path + '/clr/')
train_nums = match.load_nums(path + '/num/')

### ---- MAIN LOOP ---- ###
# The main loop repeatedly grabs frames from the video stream
# and processes them to find and identify playing cards.

BKG_THRESH = 120

person = {'l':14, 'r':1411}

card_width = 85
card_height = 118

gap_x = 101
gap_y = 131

card3_1_x = 4
card3_1_y = 265

y_pos = 14

frame = 0

quit = 0  # Loop control variable

# Begin capturing frames
while quit == 0:
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    img = videostream.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    img_w, img_h = np.shape(img)[:2]
    bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
    thresh_level = bkg_level + BKG_THRESH
    ret, thresh = cv2.threshold(blur, thresh_level, 255, cv2.THRESH_BINARY_INV)

    for p_name, x_pos in person.items():
        imgCrop = thresh[y_pos:y_pos + 386, x_pos:x_pos + 494]

        for i in range(3):
            y = card3_1_y - i * gap_y
            for j in range(5):
                x = card3_1_x + j * gap_x
                card = imgCrop[y:y + card_height, x:x + card_width]
                card_clr = card[3:43, 3:37]
                card_clr[36:43, 27:37] = 0
                card_num = card[39:114, 30:82]

                clr = match.match(card_clr, train_clrs, CLR_DIFF_MAX)
                num = match.match(card_num, train_nums, NUM_DIFF_MAX)

                img = match.draw_results(img, clr, num, x_pos + x, y_pos + y)
                # cv2.drawContours(img, temp_cnts, -1, (255, 0, 0), 2)

    cv2.putText(img, "FPS: " + str(int(frame_rate_calc)), (10, 26), font, 0.7, (255, 0, 255), 2, cv2.LINE_AA)

    # Finally, display the image with the identified cards!
    cv2.imshow("Card Detector", img)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1

    frame += 1

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1

# Close all windows and close the PiCamera video stream.
cv2.destroyAllWindows()
videostream.stop()

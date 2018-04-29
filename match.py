import cv2
import numpy as np

## Define font to use
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

class Train_suits:
    def __init__(self):
        self.img = [] # Thresholded, sized suit image loaded from hard drive
        self.name = "Placeholder"

def load_clrs(filepath):
    """Loads suit images from directory specified by filepath. Stores
    them in a list of Train_suits objects."""

    train_suits = []
    i = 0

    for Suit in ['spades', 'diamonds', 'clubs', 'hearts']:
    # for Suit in ['♧', '♢', ]
        train_suits.append(Train_suits())
        train_suits[i].name = Suit
        filename = Suit + '.png'
        train_suits[i].img = cv2.imread(filepath + filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return train_suits


def load_nums(filepath):
    """Loads suit images from directory specified by filepath. Stores
    them in a list of Train_suits objects."""

    train_suits = []
    i = 0

    for Suit in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', "jok"]:
        train_suits.append(Train_suits())
        train_suits[i].name = Suit
        filename = Suit + '.png'
        train_suits[i].img = cv2.imread(filepath + filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return train_suits


def match(img, train, max_diff):
    """Finds best rank and suit matches for the query card. Differences
    the query card rank and suit images with the train rank and suit images.
    The best match is the rank or suit image that has the least difference."""

    best_match_diff = 10000
    best_match_name = "Unknown"
    matched = ""
    i = 0

    for t in train:

        diff_img = cv2.absdiff(img, t.img)
        diff = int(np.sum(diff_img) / 255)

        if diff < best_match_diff:
            best_match_diff = diff
            best_match_name = t.name


    # Combine best rank match and best suit match to get query card's identity.
    # If the best matches have too high of a difference value, card identity
    # is still Unknown
    if (best_match_diff < max_diff):
        matched = best_match_name

    # Return the identiy of the card and the quality of the suit and rank match
    return matched


def draw_results(image, clr, num, x, y, xpos, ypos, width_ratio, height_ratio):
    """Draw the card name, center point, and contour on the camera image."""

    if clr == "err":
        print("lhh")
    cv2.circle(image, (x, y), 5, (255, 0, 0), -1)

    # Draw card name twice, so letters have black outline
    cv2.putText(image, clr, (x + int((xpos + 25) * width_ratio), y + int((ypos + 20) * height_ratio)), font, 1, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(image, clr, (x + int((xpos + 25) * width_ratio), y + int((ypos + 20) * height_ratio)), font, 1, (50, 200, 200), 2, cv2.LINE_AA)

    cv2.putText(image, num, (x + int((xpos + 40) * width_ratio), y + int((ypos + 20) * height_ratio)), font, 1, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(image, num, (x + int((xpos + 40) * width_ratio), y + int((ypos + 20) * height_ratio)), font, 1, (50, 200, 200), 2, cv2.LINE_AA)

    return image
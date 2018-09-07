# -*- coding: utf-8 -*-
 
import cv2  
import numpy as np
import matplotlib.pyplot as plot
import dlib
import time
import sys

PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
SCALE_FACTOR = 1 
FEATHER_AMOUNT = 11

# FACE_POINTS = list(range(17, 68))
# MOUTH_POINTS = list(range(48, 61))
# RIGHT_BROW_POINTS = list(range(17, 22))
# LEFT_BROW_POINTS = list(range(22, 27))
# RIGHT_EYE_POINTS = list(range(36, 42))
# LEFT_EYE_POINTS = list(range(42, 48))
# NOSE_POINTS = list(range(27, 35))
# JAW_POINTS = list(range(0, 17))
FACE_POINTS = (range(17, 68))
MOUTH_POINTS = (range(48, 61))
RIGHT_BROW_POINTS = (range(17, 22))
LEFT_BROW_POINTS = (range(22, 27))
RIGHT_EYE_POINTS = (range(36, 42))
LEFT_EYE_POINTS = (range(42, 48))
NOSE_POINTS = (range(27, 35))
JAW_POINTS = (range(0, 17))
# Points used to line up the images.
ALIGN_POINTS = (LEFT_BROW_POINTS + RIGHT_EYE_POINTS + LEFT_EYE_POINTS +
                               RIGHT_BROW_POINTS + NOSE_POINTS + MOUTH_POINTS)

# Points from the second image to overlay on the first. The convex hull of each
# element will be overlaid.
OVERLAY_POINTS = [
    LEFT_EYE_POINTS + RIGHT_EYE_POINTS + LEFT_BROW_POINTS + RIGHT_BROW_POINTS,
    NOSE_POINTS + MOUTH_POINTS,
]

# Amount of blur to use during colour correction, as a fraction of the
# pupillary distance.
COLOUR_CORRECT_BLUR_FRAC = 0.6

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)


def draw_convex_hull(im, points, color):
    print points
    points = cv2.convexHull(points)
    cv2.fillConvexPoly(im, points, color=color)

def get_face_mask(im, landmarks):
    im = np.zeros(im.shape[:2], dtype=np.float64)
    print landmarks
    for group in OVERLAY_POINTS:
        print group[0]
        print group[len(group)-1]
        print group
        draw_convex_hull(im,
                         landmarks[min(group):max(group)],
                         color=1)

    im = np.array([im, im, im]).transpose((1, 2, 0))

    im = (cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0) > 0) * 1.0
    im = cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0)

    return im

def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords

def transformation_from_points(points1, points2):
    """
    Return an affine transformation [s * R | T] such that:
        sum ||s*R*p1,i + T - p2,i||^2
    is minimized.
    """
    # Solve the procrustes problem by subtracting centroids, scaling by the
    # standard deviation, and then using the SVD to calculate the rotation. See
    # the following for more details:
    #   https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem

    points1 = points1.astype(np.float64)
    points2 = points2.astype(np.float64)

    c1 = np.mean(points1, axis=0)
    c2 = np.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2

    s1 = np.std(points1)
    s2 = np.std(points2)
    points1 /= s1
    points2 /= s2

    U, S, Vt = np.linalg.svd(points1.T * points2)

    # The R we seek is in fact the transpose of the one given by U * Vt. This
    # is because the above formulation assumes the matrix goes on the right
    # (with row vectors) where as our solution requires the matrix to be on the
    # left (with column vectors).
    R = (U * Vt).T

    return np.vstack([np.hstack(((s2 / s1) * R,
                                       c2.T - (s2 / s1) * R * c1.T)),
                         np.matrix([0., 0., 1.])])

def resize_width(image, num):
    height, width = image.shape[:2]  
    size = (int(width*num), int(height*num))  
    resized = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    return resized

def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x 
    h = rect.bottom() - y 
    return (x, y, w, h)    

def face_finder(image, zoom):
    raw_size = image.shape

    image = resize_width(image, zoom)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    
    i = 0
    shapes = []
    for rect in rects:
        shape = predictor(gray, rect)
        shape = shape_to_np(shape)
        shapes.append(shape)
    return shapes


gap = 5
zoom = 1
cap = cv2.VideoCapture(0)
cnt = gap
image2 = cv2.imread(sys.argv[1])
shapes2 = face_finder(image2, zoom)
landmarks2 = shapes2[0]

mask = get_face_mask(image2, landmarks2)

while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    if gap==cnt:
        time0 = time.time()
        shapes = face_finder(frame, zoom)
        cnt = 0
        print time.time()-time0
    cnt = cnt + 1
    for landmarks1 in shapes:
        M = transformation_from_points(landmarks1[ALIGN_POINTS],
                               landmarks2[ALIGN_POINTS])
        warped_mask = warp_im(mask, M, frame.shape)

        # i = 0
        # for (x, y) in shape:
            # cv2.rectangle(frame, (x, y), (x+1, y+1), (127,255,127), 2)
            # i = i + 1
        # print shape

    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 

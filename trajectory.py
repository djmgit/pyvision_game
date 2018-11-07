import pygame
import numpy as np
import cv2
import math

from collections import deque
from imutils.video import VideoStream
import argparse
import imutils
import time

import random

pygame.init()
clock = pygame.time.Clock()
vs = cv2.VideoCapture(0)


white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

display_width = 800
display_height = 800

line = []

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay.fill(white)


def draw_line():
    if len(line) <= 1:
        return
    prev = line[0]
    for point in line[1:]:
        curr = point
        pygame.draw.line(gameDisplay, blue, prev, curr, 5)
        prev = curr

def draw_tracker(x, y, r):
    pygame.draw.circle(gameDisplay, blue, (x, y), 20)

def eq_straight_line(x, m, c):
    return (x * m) + c

def circle(x, r):
    y = math.sin(x)
    return y

def get_rand_dir(delta):
    drc = [-1, 1]
    index = random.randrange(0, 2)
    return drc[index] * delta

def draw_bar(x, y, width, height):
    pygame.draw.rect(gameDisplay, red, (x, y, width, height))

def check_collision(ball_x, ball_y, bar_x, bar_y, r):
    if ((ball_y + r) >= bar_y) and ((ball_x - r >= bar_x) and (ball_x + r <= bar_x + bar_width)):
        return True
    return False

def process_frame(frame):
    # process the captured frame
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            return x, y, center
    return None



x = int(display_width / 2)
y = int(display_height / 2)
delta_x = 2
delta_y = -5
r = 20
bar_x = int(display_width / 2)
bar_y = int(0.75 * display_height)
bar_delta_x = 0
bar_width = 100
bar_height = 40
while True:
    ret, frame = vs.read()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if bar_x >= 0:
                    bar_delta_x = -10
                else:
                    bar_delta_x = 0

            if event.key == pygame.K_RIGHT:
                if bar_x + bar_delta_x <= display_width:
                    bar_delta_x = 10
                else:
                    bar_delta_x = 0
#
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                bar_delta_x = 0

    #print (x, y)
    gameDisplay.fill(white)

    res = process_frame(frame)
    if (res):
        bar_x = res[0]

    cv2.imshow('frame',frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        pygame.quit()
        break

    draw_tracker(x, y, r)
    draw_bar(bar_x, bar_y, bar_width, bar_height)
    bar_x += bar_delta_x

    if ((y + (1 * r)) >= display_height) or (y <= 0):
        delta_y = -1 * delta_y
        delta_x = get_rand_dir(delta_x)

    if ((x + (1 * r)) >= display_width) or (x <= 0):
        delta_x = -1 * delta_x
        delta_y = get_rand_dir(delta_y)

    if check_collision(x, y, bar_x, bar_y, r):
        delta_y = -1 * delta_y
        delta_x = get_rand_dir(delta_x)

    x += delta_x
    y += delta_y


    pygame.display.update()
    clock.tick(60)

vs.release()
cv2.destroyAllWindows()

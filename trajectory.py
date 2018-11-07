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
    print (x, y)
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

def process_freme(frame):
    # process the captured frame
    pass


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

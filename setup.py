import pygame
import random
import math
import time
import numpy as np
from RLE_decoder import decode
import psutil
import tkinter as tk
from tkinter import filedialog

# Initialise pygame
pygame.init()

# Set the dimensions of the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 640
dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)
center = pygame.Vector2(dimensions) / 2
V_ZERO = pygame.Vector2(0, 0)


# Set the name and icon of the window
pygame.display.set_caption("Conway's Game of Life")
icon = pygame.image.load("logo.ico")
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)

# Find out delta and create clock
clock = pygame.time.Clock()
fps = 30


class Colour:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (127, 127, 127)
    DARK_GRAY = (40, 40, 40)
    DARK_DARK_GRAY = (20, 20, 20)
    LIGHT_GRAY = (225, 225, 225)
    RED = (204, 0, 0)

# Set the dimensions of the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

from menu import PopUp2
from label import Label, Button, Slider

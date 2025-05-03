#!/bin/python3

#Setting file
import os
NAME = "FuRoku"

"""Display Settings"""
resolutionWidth = 1920 
resolutionHeight = 1080
#resolutionWidth, resolutionHeight = info.current_w, info.current_h
# os.environ['SDL_VIDEO_CENTERED'] = '12'
WINDOW_SIZE = (resolutionWidth, resolutionHeight)
FPS = 60

"""Defines Colors for Objects"""

# Base Colors 
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)

#Variant Colors
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 150, 255)
DARK_BLUE = (10, 10, 74)
DARK_BLUE_TRANS = (0, 0, 25, 100)
TEXT_COLOR = BLACK
BLUE_ISH = (100, 100, 200)  # Blue-ish


"""Settings looks of menus and buttons"""
#THEME
RADIUS = 20
MENU_BG_COLOR = DARK_BLUE_TRANS 
BUTTON_COLOR = BLUE_ISH
BUTTON_BG_COLOR = DARK_BLUE_TRANS

#Font Settings 
FONT_SIZE = 30

# ASSETS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
"""Defines the location of Asset files"""
FONT_PATH = os.path.join(BASE_DIR, "Assets", "Fonts", "GoMonoNerdFont-Bold.ttf")
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "Assets", "Images", "background2.jpg")
TEST_BUTTON_IMAGE = os.path.join(BASE_DIR, "Assets", "Images", "testing.png")
MUSIC = os.path.join(BASE_DIR, "Assets", "Sound", "Music","space-trip.mp3")
CLICK_SOUND = os.path.join(BASE_DIR, "Assets", "Sound", "click.mp3")
APPS_PATH = os.path.join(BASE_DIR, "apps.json")

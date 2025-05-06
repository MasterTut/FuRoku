from os import wait
import pygame 
from typing import List, Optional, Dict

#Custom Import 
from settings import *


#Init
Mixer = pygame.mixer
Mixer.init()
pygame.init()
Canvas = pygame.display.set_mode((WINDOW_SIZE), pygame.RESIZABLE)
background_img  = pygame.image.load(BACKGROUND_IMAGE).convert()
background_img = pygame.transform.scale(background_img, (resolutionWidth, resolutionHeight))
background_position = (0, 0)
Font = pygame.font.Font(FONT_PATH, FONT_SIZE)


class Menu:
    """Defines what a menu is and does"""
    def __init__(self, x, y, width, height, name='unnamed') -> None:
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.background = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_active = False
        self.is_list = True
        self.menu_list: List[str]= []
        self.button_matrix:  List[List[Button]] = [[]]
        self.input_boxes = []
        self._nested_menu_map: dict = {}
    def display_input_boxes(self):
        for input in self.input_boxes:
            input.display()
    def display_buttons(self):
        for button in self._get_all_buttons():
            button.display()
    
    def display(self):
        if self.button_matrix:
            self.display_buttons()
        if self.input_boxes:
            self.display_input_boxes()
        Canvas.blit(self.surface, self.rect)
        self.display_background()
    def display_background(self):
        """"Displays a transparnet background if set to true else clears the background to update display"""
        if self.background == True:
            pygame.draw.rect(self.surface, MENU_BG_COLOR, self.rect, border_radius=RADIUS)
        else:
            #clear menu
            pygame.draw.rect(self.surface, (0,0,0,0), self.rect)
    
    def _get_total_buttons_count(self):
        """this is used to determine movement how many rows to create and movement on menu"""
        total_buttons = 0
        for row in self.button_matrix:
            total_buttons += len(row)
        return total_buttons
    def _get_all_buttons(self):
        """Loops through button matrix and appends all to a single list"""
        all_buttons = []
        rows = len(self.button_matrix)
        for row in range(0, rows): 
            for button in self.button_matrix[row]:
                all_buttons.append(button)
        return all_buttons
    
    def _get_active_button_idx_row(self):
        """get active button idx and row"""
        idx = 0
        row = 0
        for array in self.button_matrix:
            for button in array:
                if button.is_active:
                    row = self.button_matrix.index(array)
                    idx = array.index(button)
        return idx, row
    

class Button:
    def __init__(self, x, y, width, height, menu:Menu, name='unnamed'):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_active = False
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.menu_surface = menu.surface
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #Set Text Front if button is Text Only
        self.text = Font.render(name, True, (255,200,200))
        self.text_highlighted = Font.render(name, True, (255, 255, 200))
        #Set Image if button is image
        self.is_image = False
        self.image = pygame.image.load(TEST_BUTTON_IMAGE)
        self.cmd = "test" 
    
    def action(self):
        """define the action the button takes when clicked or enter is pressed"""
        print(self.name)
        #os.system("librewolf")

    def display_text(self):
        """hightlight text when selected"""
        self.menu_surface.blit(self.surface, self.rect)
        if self.is_active:
          self.menu_surface.blit(self.text_highlighted, self.rect)
        else:
          self.menu_surface.blit(self.text, self.rect)

    def display_image(self):
        """display image of button"""
        padding = 5
        #draw background for Apps 
        pygame.draw.rect(self.menu_surface, (BUTTON_BG_COLOR), 
                         (self.rect.x - padding, 
                          self.rect.y - padding, 
                          self.image.get_width() + 2 * padding, 
                          self.image.get_height() + 2 * padding))
        
        if self.is_active:
            size = self.image.get_size()
            if size == (48, 48):
                scaled_image = pygame.transform.scale2x(self.image) 
            elif size == (256, 256):
                scaled_image = pygame.transform.smoothscale(self.image, (300,300))
            else:
                #This is just to ensure scaled_image is returned may change this later to include other image sizes
                scaled_image = pygame.transform.smoothscale(self.image, (300,300))
            self.menu_surface.blit(scaled_image, (self.rect.x -22, self.rect.y -25))
            #mouse_pos = pygame.mouse.get_pos()
            #print("Mouse is at:", mouse_pos)
            #print(self.name, self.rect.x, self.rect.y)
            
        else:
            self.menu_surface.blit(self.image, self.rect)
    def display(self):
        if self.is_image:
            self.display_image()
        else:
            self.display_text()



class TextInput:
    def __init__(self, x, y, width, height, menu:Menu, name="Default") -> None:
        self.name = name
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.menu = menu
        self.is_selected = False
        self.color = (0, 0, 0)
        self.name_surface = Font.render(f"{self.name}: ", True, (0, 0, 0))
        self.nameX = self.x - self.name_surface.get_width() - 5  # Position to the left of the box
        self.nameY = self.y + (self.height - self.name_surface.get_height()) // 2  # Center vertically
        self.text = ""
        self.text_surface = Font.render(self.text, True, (0, 0, 0))
        self.textX = self.x + 5  # Small padding inside the box
        self.textY = self.y + (self.height - self.text_surface.get_height()) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def update_text(self):
         #Update the text surface when text changes
        self.text_surface = Font.render(self.text, True, (0, 0, 0))
        self.textY = self.y + (self.height - self.text_surface.get_height()) // 2  # Recenter vertically
    def display(self):
        if self.is_selected:
            self.color = (0, 255, 0)
        else:
            self.color = (0, 0, 0)
        
        # Adjust rect position to align with name text
        self.rect = pygame.Rect(self.x, self.nameY, self.width, self.height)
        pygame.draw.rect(self.menu.surface, self.color, self.rect, 2)
        
        # Draw the input text inside the box (separate from name)
        self.menu.surface.blit(self.name_surface, (self.nameX, self.nameY))
        self.menu.surface.blit(self.text_surface, (self.textX, self.textY))



class ErrorWindow:
    def __init__(self,x, y, message="unknown"):
        self.x = x
        self.y = y
        self.width = Canvas.get_width() / 2
        self.height = Canvas.get_height() / 2
        self.surface = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.button = Button(self.width -50, self.height -50, 20, 20, self.surface, name="OK")  
        self.message = message
        self.error = False 
        self.button.action = self.ok_button_func
    def display(self):
        """Display the error window, with error""" 
        self.message = str(self.message) if self.message is not None else "Unknown error"
        self.surface.fill((0,0,0,100))
        text_y = 10
        for line in self.wrap_text(self.message):
            text_surface = Font.render(line, True, RED)
            self.surface.blit(text_surface, (10,text_y))
            text_y += 30
        self.button.display()
        Canvas.blit(self.surface, (self.x, self.y))
    def wrap_text(self, message):
        """Wrap text to fit within max_width on a surface."""
        words = message.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            text_surface = Font.render(test_line, True, (0, 0, 0))
            if text_surface.get_width() <= self.width -10:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines
    def ok_button_func(self):
        self.button.is_active = False
        self.error = False 

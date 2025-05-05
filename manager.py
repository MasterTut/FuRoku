#!/bin/python3
from os import wait
from re import sub
import sys
import json

#custom imports 
from settings import *
from components import *
from enum import Enum

import settings 


class MenuManager:
    """Intialize menus and keeps track of active Menus"""
    def __init__(self) -> None:
        #Defining the root menu (side_menu) 
        self.side_menu = Menu(0, 20, 300, Canvas.get_width() - 40, name="side_menu")
        self.side_menu.is_list = True
        self._all_menus: Dict[Menu, List[Menu]] = {self.side_menu : []} 
        self.side_menu.menu_list = self.read_file()
        self.buttons_of_menu_names(self.side_menu)
        #adding setting button to Side_menu
        self.settings_button = Button(self.side_menu.width * .2, 1000, 256, 256, self.side_menu, "settings")
        self.side_menu.button_matrix[0].append(self.settings_button)
        #Adding a Default Menu in case there is any bugs, need to add error blit to screen
        self.default_menu = Menu(Canvas.get_width() * .19, 0, Canvas.get_width(), Canvas.get_height() -40,'defaultMenu')
        self.default_button = Button(0,0,256,256,self.default_menu, "default_button")
        self._selected_menu = next(iter(self._all_menus), self.default_menu)
        self._selected_button = (self._selected_menu.button_matrix[0][0] if self._selected_menu and self._selected_menu.button_matrix else self.default_button)
    


    def buttons_of_menu_names(self,menu:Menu, button_width: int = 150, button_height: int = 40, vertical_spacing: int = 50) -> None:
        """Create buttons from menu_list for list-based menus."""
        if not menu.is_list:
            return
        self.button_matrix = [[]]
        y_offset = 30
        x_pos = menu.width * 0.2
        for button_text in menu.menu_list:
            button = Button(x_pos, y_offset, button_width, button_height, menu, button_text)
            menu.button_matrix[0].append(button)
            y_offset += vertical_spacing
    
    def import_apps(self, menu_name, apps_list):
        """Import Menus and Image Buttons from json example: Apps { Name: Netflix, CMD: chromium..."""
        new_menu = Menu(Canvas.get_width() * .10, 0, Canvas.get_width(), Canvas.get_height(), menu_name)
        #new_menu = Menu(200, 20, 1920, 1080, menu_name)
        new_menu.is_list = False
        new_menu.background = False
        padding = 31
        button_width = 256
        button_height = 256
        max_width = new_menu.width - (padding + button_width)
        buttons_per_row = max_width // (button_width + padding)
        # Calculate grid dimensions
        total_buttons = len(apps_list)
        rows = (total_buttons + buttons_per_row - 1) // buttons_per_row  # Ceiling division

        x_start = new_menu.x + 50

        # Create a 2D matrix
        new_menu.button_matrix = [[] for _ in range(rows)]
        for i, app in enumerate(apps_list):
            row = i // buttons_per_row
            col = i % buttons_per_row
            x = x_start + col * (button_width + padding)
            y = padding + row * (button_height + padding)
            new_button = Button(x, y, button_width, button_height,new_menu, app['name'])
            new_button.image = pygame.image.load(app['image'])
            new_button.image = pygame.transform.scale(new_button.image, (button_width, button_height))
            new_button.cmd = app['cmd']
            new_button.is_image = True
            new_menu.button_matrix[row].append(new_button)

        self._all_menus.setdefault(self.side_menu, []).append(new_menu)
    
    def read_file(self):
        """reads apps.json and send to import apps"""
        custom_menu_names = [] 

        if not os.path.exists(APPS_PATH):
            print("apps.json not found, creating a default file.")
            default_data = {"apps": [{"name": "defaultApp", "image": "./Assets/defaultApp.png", "cmd": "echo 'hello'"}]}
            with open(APPS_PATH, 'w') as f:
                json.dump(default_data, f, indent=2)

        with open(APPS_PATH, 'r') as apps:
            data = json.load(apps)
        for menu_name in data:
            apps = []
            custom_menu_names.append(menu_name)
            for app in data[menu_name]:
                apps.append(app)
            self.import_apps(menu_name, apps) 
        return custom_menu_names

    def _display_menus(self):
        for menu in self._all_menus:
            if menu.is_active:
                menu.display()
        for submenu in self._all_menus[self.side_menu]:
            if self._selected_button.name == submenu.name or submenu == self._selected_menu:
                submenu.is_active = True
                submenu.display()
            else:
                submenu.is_active = False
    def _get_all_menus(self):
        """returns a list of all menus"""
        list_menu = []
        for menu in self._all_menus:
            list_menu.append(menu)
            for submenu in self._all_menus[menu]:
                list_menu.append(submenu)
        return list_menu

   
class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class Manager:
    """Tells MenuManager what Menu is selected and implments controls for moving on screen"""
    def __init__(self) -> None:
        self.menu_mgr = MenuManager()
        self.sound = Mixer.Sound(CLICK_SOUND)
    
    def listener(self):
        """Listen for keyboard and mouse input and sends to Move function"""
        self.total_buttons = self.menu_mgr._selected_menu._get_total_buttons_count()
        if self.total_buttons > 0:
            self.button_index, self.row = self.menu_mgr._selected_menu._get_active_button_idx_row()
            self.total_rows = len(self.menu_mgr._selected_menu.button_matrix)
            self.col = self.button_index % self.total_buttons
        self.menu_mgr._selected_button.is_active = True
        self.menu_mgr._selected_menu.is_active = True
        for event in pygame.event.get():

              if event.type == pygame.QUIT:
                  sys.exit()
              if event.type == pygame.MOUSEMOTION:
                    self._track_mouse_movement()
              if event.type == pygame.MOUSEBUTTONDOWN:
                  #track mouse clicks 
                  mouse_pos = pygame.mouse.get_pos()
              #TRACK IF INPUT FIELD IS SELECTED 
              elif event.type == pygame.TEXTINPUT:
                  pass
                  
              #TRACK KEY PRESSES
              elif event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_ESCAPE:
                      sys.exit()
                  self.move(event.key)
    
    def move(self, key) -> None:
        """Menus and button naviagtion"""

        self.sound.play()
        if key == pygame.K_RIGHT:
            if self.menu_mgr._selected_menu.is_list:
                self._switch_menu()
            else:
                self._move_in_grid(Direction.RIGHT)
            print("RIGHT")
        if key == pygame.K_LEFT:
            if self.menu_mgr._selected_menu.is_list:
                return
            else: 
                self._move_in_grid(Direction.LEFT)
            print("LEFT")
        if key == pygame.K_DOWN:
            if self.menu_mgr._selected_menu.is_list:
                self._move_list(Direction.DOWN )
            else:
                self._move_in_grid(Direction.DOWN)
            print("DOWN")
        if key == pygame.K_UP:
            if self.menu_mgr._selected_menu.is_list:
                self._move_list(Direction.UP )
            else:
                self._move_in_grid(Direction.UP)
            print("UP")
        if key == pygame.K_RETURN:
            print("ENTER")
    
    def _move_list(self, direction:Direction):
        """move up or down on list menu"""
        if direction == Direction.UP:
            self.button_index = (self.button_index -1) if self.button_index > 0  else self.total_buttons -1 
        if direction == Direction.DOWN:
            self.button_index = (self.button_index +1) if self.button_index + 1 < self.total_buttons else 0 
        
        self.menu_mgr._selected_button = self.menu_mgr._selected_menu.button_matrix[0][self.button_index]
        self._deselect_buttons(self.menu_mgr._selected_menu)
    
    def _switch_menu(self):
        """Switch from List Menu to nested Menu"""
        if self.menu_mgr._all_menus[self.menu_mgr._selected_menu]:
            for menu in self.menu_mgr._all_menus[self.menu_mgr._selected_menu]:
                if menu.button_matrix and menu.name ==self.menu_mgr._selected_button.name:
                    self.menu_mgr._selected_menu = menu
                    self._select_first_item()

    def _deselect_buttons(self, menu):
        """Deselect all buttons that are not currenlty selected"""
        for row in menu.button_matrix:
            for button in row:
                if button != self.menu_mgr._selected_button:
                    button.is_active = False
    
    def _deselect_menus(self):
        """Deselect all menus that are not currenlty selected"""
        for menu in self.menu_mgr._all_menus:
            if menu != self.menu_mgr._selected_menu:
                menu.is_active = False
            for submenu in self.menu_mgr._all_menus[menu]:
                if submenu != self.menu_mgr._selected_menu:
                    submenu.is_active = False
    
    def _select_side_menu(self):
        """Selects the side menu"""
        self._deselect_buttons(self.menu_mgr._selected_menu)
        self.menu_mgr._selected_menu = self.menu_mgr.side_menu
        self._select_first_item()

    
    def _select_first_item(self) -> None:
        """Select the first button or input box in the active menu."""
        self.menu_mgr._selected_button.is_active = False
        if self.menu_mgr._selected_menu.button_matrix: 
            self.menu_mgr._selected_button = self.menu_mgr._selected_menu.button_matrix[0][0]
        elif self.menu_mgr._selected_menu.input_boxes:
            self.menu_mgr._selected_button = self.menu_mgr._selected_menu.input_boxes[0]


    def _move_in_grid(self, direction: Direction ) -> None:
        """Handle navigation in a grid menu."""
                                                                                            
        if direction == Direction.UP:
            self.row = (self.row - 1) if self.row > 0 else self.total_rows - 1
        elif direction == Direction.DOWN:
            self.row = (self.row + 1) if self.row + 1 < self.total_rows else 0
        elif direction == Direction.RIGHT:
            if self.menu_mgr._selected_button:
                self.menu_mgr._selected_button.is_active = False
            if self.col + 1 < len(self.menu_mgr._selected_menu.button_matrix[self.row]):
                self.col += 1
        elif direction == Direction.LEFT:
            if self.col > 0:
                self.col -= 1
            else:
                return self._select_side_menu()
                
        # Ensure valid button selection
        if len(self.menu_mgr._selected_menu.button_matrix[self.row]) > self.col:
            self.menu_mgr._selected_button = self.menu_mgr._selected_menu.button_matrix[self.row][self.col]
        else:
            self.menu_mgr._selected_button = self.menu_mgr._selected_menu.button_matrix[self.row][-1]
        self.menu_mgr._selected_button.is_active = True
        self._deselect_buttons(self.menu_mgr._selected_menu)

    
    def _track_mouse_movement(self):
        mouse_pos = pygame.mouse.get_pos()
        selected_menu = self.menu_mgr._selected_menu
        #Need to offset the mouse position as mouse postion tracks Canvas pos not and butons are draw in corliation with the Surface
        surface_mouse_pos = (mouse_pos[0] - selected_menu.x, mouse_pos[1] - selected_menu.y)
        all_buttons = self.menu_mgr._selected_menu._get_all_buttons()
        for menu in self.menu_mgr._get_all_menus():
            if menu.rect.collidepoint(mouse_pos) and menu.is_active:
                self.menu_mgr._selected_menu = menu
        for button in all_buttons:
            if button.rect.collidepoint(surface_mouse_pos):
                self.menu_mgr._selected_button = button                     
                self._deselect_buttons(self.menu_mgr._selected_menu)        

        
                        



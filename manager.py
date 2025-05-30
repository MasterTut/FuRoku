#!/bin/python3
from os import wait
import sys
import json
from enum import Enum
#custom imports 
from menus import *
import menus
from settings import *
from components import *

class MenuManager:
    """Intialize menus and keeps track of active Menus"""
    def __init__(self) -> None:
        #Defining the base menu (side_menu) 
        self.side_menu = Menu(0, 0,Canvas.get_width(), Canvas.get_height(), name="side_menu")
        self.side_menu.is_button_list = True
        self.side_menu.is_active = True
        self.add_list_of_menu_names_to_side_menu()
        #self._import_apps_to_settings_menu()
        self.side_menu.sub_menus[-1].sub_menus.append( menus.import_app_customization_menus())
        self._import_apps_to_settings_menu()
        #keep track of what is currently selected, in listener the menu and button are activated and de-activated
        self._selected_menu: Menu = self.side_menu
        self._selected_button: Button = self.side_menu.button_matrix[0][0]
        self._all_selected_buttons: list[Button] = []
        self._all_menus = self._get_all_menus()
        menus._import_apps_to_settings_menu(self)

    def add_list_of_menu_names_to_side_menu(self, button_width: int = 150, button_height: int = 40, vertical_spacing: int = 50) -> None:
        """Create buttons from list of button names for list-based menus."""
        menu = self.side_menu
        y_offset = 90
        x_pos = 50
        for button_text in self.read_file():
            #Change option for Settings
            if button_text == "SETTINGS":
                y_pos = (menu.height * .9)
                button = Button(x_pos + 35, y_pos, button_width, button_height, menu, name=button_text)
                button.background = False
                button.image = pygame.image.load(SETTINGS_GEAR)
                button.is_image = True
                
            else:
                button = Button(x_pos, y_offset, button_width, button_height, menu, name=button_text)
                button.select_rectangle = True
                button.background =False
            menu.button_matrix[0].append(button)
            y_offset += vertical_spacing
    
    def import_apps(self, menu_name, apps_list) -> None:
        """Import Menus and Image Buttons from json example: Apps { Name: Netflix, CMD: chromium..."""
        x_pos = int(Canvas.get_width() * .15)
        width = int(Canvas.get_width() - (x_pos +50))
        
        new_menu = Menu(x_pos, 0, width, Canvas.get_height(), menu_name)
        new_menu._set_buttons(apps_list, button_width=256, button_height=256)
        self.side_menu.sub_menus.append(new_menu)
    
    def read_file(self):
        """reads apps.json and send to import apps"""
        custom_menu_names = [] 

        if not os.path.exists(APPS_PATH):
            print("apps.json not found, creating a default file.")
            default_data = {"apps": [{"name": "defaultApp", "image": "./Assets/defaultApp.png", "action": "echo 'hello'"}]}
            with open(APPS_PATH, 'w') as f:
                json.dump(default_data, f, indent=2)

        with open(APPS_PATH, 'r') as apps:
            data = json.load(apps)
        for menu_name in data:
            custom_menu_names.append(menu_name)
            self.import_apps(menu_name, data[menu_name]) 
        return custom_menu_names

        
    def _display_menus(self):
        self.side_menu.display()
        for menu in self.side_menu.sub_menus:
            if self._selected_button.name == menu.name:
                #check to ensure this is a sidemenu button > 
                if self._selected_button in self.side_menu.button_matrix[0]:
                    menu.is_active = True
            elif menu == self._selected_menu:
                menu.is_active = True
            else:
                menu.is_active = False
            
            menu.display()
                

    def _get_all_menus(self) -> List[Menu]:
        """Returns a list of all menus, including all nested submenus."""
        menu_list: List[Menu] = [self.side_menu]

        # Iterate over top-level menus
        for menu in self.side_menu._get_all_submenus():
            menu_list.append(menu)
        
        return menu_list

            
    def _import_apps_to_settings_menu(self):
        """"Import menus to display for buttons on settings menu"""
        settings_menu = self.side_menu.sub_menus[-1]
        #moved this functionality to menus.py but keeping it here for now as well
        for submenu in settings_menu.sub_menus:
            def _activate_menu():
                self._selected_menu = submenu
                submenu.is_active = True
                self._selected_menu = self._selected_menu.sub_menus[0]
                self.side_menu.is_locked = True
                for menu in submenu._get_all_submenus():
                    menu.is_active = True
            for button in settings_menu._get_all_buttons():
                if button.name ==  submenu.name:
                    button.action = _activate_menu 
    
    def _get_all_active_buttons(self):
        """Set a list of all currenltly active buttons on selected menu"""
        menu = self._selected_menu
        selected_buttons: list[Button]= []
        for row in menu.button_matrix:
           for button in row:
               if button.is_active:
                   selected_buttons.append(button)
        self._all_selected_buttons = selected_buttons
            
   
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
        self.menu_index =0
    def listener(self):
        """Listen for keyboard and mouse input and sends to Move function"""
        self.total_buttons = self.menu_mgr._selected_menu._get_total_buttons_count()
        self.total_menus = len(self.menu_mgr._selected_menu.sub_menus) if self.menu_mgr._selected_menu.is_menu_list else 0
        if self.total_buttons > 0:
            self.button_index, self.row = self.menu_mgr._selected_menu._get_active_button_idx_row()
            self.total_rows = len(self.menu_mgr._selected_menu.button_matrix)
            self.col = self.button_index % self.total_buttons
        if self.menu_mgr._selected_button.is_active == False:
            self.sound.play()
            self.menu_mgr._selected_button.is_active = True
        if self.menu_mgr._selected_button.select_rectangle:
            #Draws a Rectangle over the text of the selected button
            if self.menu_mgr._selected_menu == self.menu_mgr.side_menu:
                sel_rect_x =self.menu_mgr._selected_menu.x
                sel_rect_y = self.menu_mgr._selected_button.y
                sel_rect_width = self.menu_mgr._selected_button.width + (self.menu_mgr._selected_button.width) 
                sel_rect_color = (255,255,255, 50)
                pygame.draw.rect(self.menu_mgr._selected_menu.surface, sel_rect_color, (sel_rect_x,sel_rect_y, sel_rect_width, 50), border_radius=20)
               
        for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  sys.exit()
              if event.type == pygame.MOUSEMOTION:
                    self._track_mouse_movement()
              if event.type == pygame.MOUSEBUTTONDOWN:
                  #track mouse clicks 
                  self.menu_mgr._selected_button.action()
              #TRACK IF INPUT FIELD IS SELECTED 
              elif event.type == pygame.TEXTINPUT:
                  pass
                  
              #TRACK KEY PRESSES
              elif event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_ESCAPE:
                      sys.exit()
                  self.move(event.key)
              self.menu_mgr._selected_menu.is_selected = True
              self._deselect_menus()
    
    def move(self, key) -> None:
        """Menus and button naviagtion"""
        if key == pygame.K_RIGHT:
            if self.menu_mgr._selected_menu.is_button_list:
                self._switch_menu()
            else:
                self._move_in_grid(Direction.RIGHT)
        if key == pygame.K_LEFT:
            if self.menu_mgr._selected_menu == self.menu_mgr.side_menu:
                return
            else:
                self._move_in_grid(Direction.LEFT)
        if key == pygame.K_DOWN:
            if self.menu_mgr._selected_menu.is_button_list:
                self._move_list(Direction.DOWN )
            else:
                self._move_in_grid(Direction.DOWN)
        if key == pygame.K_UP:
            if self.menu_mgr._selected_menu.is_button_list:
                self._move_list(Direction.UP )
            else:
                self._move_in_grid(Direction.UP)
        if key == pygame.K_RETURN:
            self.menu_mgr._selected_button.action()
    
    def _move_list(self, direction:Direction):
        """move up or down on list menu"""
        if direction == Direction.UP:
            self.button_index = (self.button_index -1) if self.button_index > 0  else self.total_buttons -1 
        elif direction == Direction.DOWN:
            self.button_index = (self.button_index +1) if self.button_index + 1 < self.total_buttons else 0
        self.menu_mgr._selected_button = self.menu_mgr._selected_menu.button_matrix[0][self.button_index]
        self._deselect_all_buttons()

    def _switch_menu(self):
        """Switch to nested Menu"""
        for menu in self.menu_mgr._selected_menu.sub_menus:
             if menu.is_active and len(menu.button_matrix[0])>0:
                        self.menu_mgr._selected_menu = menu
             elif menu.is_active and menu.is_menu_list:
                self.menu_mgr._selected_menu = menu.sub_menus[-1]
             self._select_first_item()

    def _deselect_all_buttons(self):
        """Deselect all buttons that are not currenlty selected"""
        menu_selected = self.menu_mgr._selected_menu
        for row in menu_selected.button_matrix:
                for button in row:
                    if button != self.menu_mgr._selected_button:
                        button.is_active = False
    
    def _deselect_menus(self):
        """Deselect all menus that are not currenlty selected"""
        for menu in self.menu_mgr._all_menus:
            if menu != self.menu_mgr._selected_menu:
                menu.is_selected = False
            for submenu in menu.sub_menus:
                if submenu != self.menu_mgr._selected_menu:
                    menu.is_selected = False
    
    def _select_side_menu(self):
        """Selects the side menu"""
        if self.menu_mgr.side_menu.is_locked:
            return
        self._deselect_all_buttons()
        self.menu_mgr._selected_menu = self.menu_mgr.side_menu
        self._select_first_item()
    
    def _select_first_item(self) -> None:
        """Select the first button or input box in the active menu."""
        if len(self.menu_mgr._selected_menu.button_matrix[0])>0: 
            self.menu_mgr._selected_button.is_active = False
            self.menu_mgr._selected_button = self.menu_mgr._selected_menu.button_matrix[0][0]
        elif self.menu_mgr._selected_menu.input_boxes:
            pass
        else:
            return
            #self.menu_mgr._selected_button = self.menu_mgr._selected_menu.input_boxes[0]

    def _move_in_grid(self, direction: Direction ) -> None:
        """Handle navigation in a grid menu."""
        selected_menu = self.menu_mgr._selected_menu
        if direction == Direction.UP:
            if self.menu_mgr._selected_menu.parent_menu.is_menu_list:
                self._move_in_menu_list(Direction.UP)
            else:
                self.row = (self.row - 1) if self.row > 0 else self.total_rows - 1
        elif direction == Direction.DOWN:
            if self.menu_mgr._selected_menu.parent_menu.is_menu_list:
                self._move_in_menu_list(Direction.DOWN)
            elif len(selected_menu.button_matrix[0]) > 0:
                self.row = (self.row + 1) if self.row + 1 < self.total_rows else 0
        elif direction == Direction.RIGHT:
            if selected_menu.is_menu_list:
                return self._switch_menu()
            elif self.col + 1 < len(selected_menu.button_matrix[self.row]):
                self.col += 1
            else:
                self.col = 0
        elif direction == Direction.LEFT:
            if self.col > 0:
                self.col -= 1
            else:
                return self._select_side_menu()

        # Ensure valid button selection
        if len(selected_menu.button_matrix[self.row]) > self.col:
            self.menu_mgr._selected_button = selected_menu.button_matrix[self.row][self.col]
        elif self.menu_mgr._selected_menu.button_matrix[self.row]:
            self.menu_mgr._selected_button = selected_menu.button_matrix[self.row][-1]

        self._deselect_all_buttons()

    def _move_in_menu_list(self, direction):
        """move up or down menus"""
        if direction == Direction.RIGHT:
            self.menu_mgr._selected_menu = self.menu_mgr._selected_menu.sub_menus[self.menu_index]
            return
        elif direction == Direction.UP:
            self.menu_index = (self.menu_index +1) if self.menu_index + 1 < self.total_menus else 0
        elif direction == Direction.DOWN:
            self.menu_index = (self.menu_index -1) if self.menu_index > 0  else self.total_menus -1 
        self.menu_mgr._selected_menu = self.menu_mgr._selected_menu.parent_menu.sub_menus[self.menu_index]

        self._select_first_item()
    
    def _track_mouse_movement(self):
        """selects menu and button based on where the mouse is on the screen"""
        mouse_pos = pygame.mouse.get_pos()
        for menu in self.menu_mgr._all_menus:
            if menu.absolute_rect.collidepoint(mouse_pos) and menu.is_active:
                if menu._get_total_buttons_count() > 0:
                    if self.menu_mgr.side_menu.is_locked and menu == self.menu_mgr.side_menu:
                           pass
                    else:
                        self.menu_mgr._selected_menu = menu

        selected_menu = self.menu_mgr._selected_menu
        
        all_buttons = selected_menu._get_all_buttons()
        for button in all_buttons:
            if button.absolute_rect.collidepoint(mouse_pos):
                self.menu_mgr._selected_button = button
                self._deselect_all_buttons()

        
                        



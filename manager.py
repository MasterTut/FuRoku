#!/bin/python3
import sys
from enum import Enum
#custom imports 
from menus import *
from settings import *
from components import *

class MenuManager:
    """Intialize menus and keeps track of active Menus"""
    def __init__(self) -> None:
        #Defining the base menu (side_menu) 
        self.side_menu: Menu = setup_side_menu(self)
        self.side_menu.is_menu_list = True
        #keep track of what is currently selected, in listener the menu and button are activated and de-activated
        self._selected_menu: Menu = self.side_menu
        self._selected_button: Button = self.side_menu.button_matrix[0][0]
        self._all_menus = self._get_all_menus()
        self.action_state = "Not_Set"
        
    def _activate_menu(self):
        for menu in self._get_all_menus():
            #do not deactivate side menu
            if menu != self.side_menu:
                if menu == self._selected_menu:
                    menu.is_selected = True
                #The side menu is locked because another menu has been activated 
                elif self.side_menu.is_locked == False:
                    menu.is_displayed = False
            menu.display()
    
    def _get_all_menus(self) -> List[Menu]:
        """Returns a list of all menus, including all nested submenus."""
        menu_list: List[Menu] = [self.side_menu]

        # Iterate over top-level menus
        for menu in self.side_menu._get_all_submenus():
            menu_list.append(menu)
        
        return menu_list

            
   
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
        self.menu_mgr._activate_menu()
        self.total_buttons = self.menu_mgr._selected_menu._get_total_buttons_count()
        if self.menu_mgr._selected_menu.parent_menu.is_menu_list:
            self.total_menus = len(self.menu_mgr._selected_menu.parent_menu.sub_menus) 
        if self.total_buttons > 0:
            self.button_index, self.row = self.menu_mgr._selected_menu._get_active_button_idx_row()
            self.total_rows = len(self.menu_mgr._selected_menu.button_matrix)
            self.col = self.button_index % self.total_buttons
        #Tells the selected button that it is selected
        if self.menu_mgr._selected_button.is_selected == False:
            self.sound.play()
            self.menu_mgr._selected_button.is_selected = True
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
                  else:
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


    def _move_in_grid(self, direction: Direction ) -> None:
        """Handle navigation in a grid menu."""
        selected_menu = self.menu_mgr._selected_menu
        has_buttons =len(selected_menu.button_matrix[0]) > 0
        if direction == Direction.UP:
            if self.menu_mgr._selected_menu.parent_menu.is_menu_list:
                return self._move_in_menu_list(Direction.UP)
            elif has_buttons:
                self.row = (self.row - 1) if self.row > 0 else self.total_rows - 1
            else:
                return
        elif direction == Direction.DOWN:
            if self.menu_mgr._selected_menu.parent_menu.is_menu_list:
                return self._move_in_menu_list(Direction.DOWN)
            elif has_buttons:
                    self.row = (self.row + 1) if self.row + 1 < self.total_rows else 0
            else:
                return
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
        self.menu_mgr._selected_button = selected_menu.button_matrix[self.row][self.col]
        self._deselect_all_buttons()

    def _move_in_menu_list(self, direction):
        """move up or down menus"""
        if direction == Direction.UP:
            self.menu_index = (self.menu_index -1) if self.menu_index > 0  else self.total_menus -1 
        if direction == Direction.DOWN:
            self.menu_index = (self.menu_index +1) if self.menu_index + 1 < self.total_menus else 0
        self.menu_mgr._selected_menu = self.menu_mgr._selected_menu.parent_menu.sub_menus[self.menu_index]
        self._select_first_last()
    
    def _switch_menu(self):
        """Switch to nested Menu"""
        for menu in self.menu_mgr._selected_menu.sub_menus:
             if menu.is_displayed and len(menu.button_matrix[0])>0:
                        self.menu_mgr._selected_menu = menu
             elif menu.is_displayed and menu.is_menu_list:
                self.menu_mgr._selected_menu = menu.sub_menus[-1]
             self._select_first_last()

    def _deselect_all_buttons(self):
        """Deselect all buttons that are not currenlty selected"""
        menu_selected = self.menu_mgr._selected_menu
        for row in menu_selected.button_matrix:
                for button in row:
                    if button != self.menu_mgr._selected_button:
                        button.is_selected = False
    
    def _deselect_menus(self):
        """Deselect all menus that are not currenlty selected"""
        for menu in self.menu_mgr._all_menus:
            if menu != self.menu_mgr._selected_menu:
                menu.is_selected = False
    
    def _select_side_menu(self):
        """Selects the side menu"""
        if self.menu_mgr.side_menu.is_locked:
            return
        self.menu_mgr._selected_menu = self.menu_mgr.side_menu
        self._select_first_last()
    
    def _select_first_last(self) -> None:
        """Select the first or previously selected button"""
        menu = self.menu_mgr._selected_menu
        if len(menu.button_matrix[0])>0: 
            self.menu_mgr._selected_button = menu.last_button_selected if menu.last_button_selected != None else menu.button_matrix[0][0]
    
    def _track_mouse_movement(self):
        """selects menu and button based on where the mouse is on the screen"""
        mouse_pos = pygame.mouse.get_pos()
        for menu in self.menu_mgr._all_menus:
            if menu.absolute_rect.collidepoint(mouse_pos) and menu.is_displayed:
                if menu._get_total_buttons_count() > 0:
                    if self.menu_mgr.side_menu.is_locked and menu == self.menu_mgr.side_menu:
                           pass
                    else:
                        self.menu_mgr._selected_menu = menu
        selected_menu = self.menu_mgr._selected_menu
        all_buttons = selected_menu._get_all_buttons()
        for button in all_buttons:
            if button.absolute_rect.collidepoint(mouse_pos):
                print('rect', mouse_pos, button.rect) 
                print('a_rect', mouse_pos, button.absolute_rect) 
                self.menu_mgr._selected_button = button
                self._deselect_all_buttons()

        
                        



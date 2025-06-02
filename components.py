import pygame 
from typing import List, Dict 
import webbrowser
#Custom Import 
from settings import *

#Init
Mixer = pygame.mixer
Mixer.init()
pygame.init()
Canvas = pygame.display.set_mode((WINDOW_SIZE), pygame.RESIZABLE)
background_img  = pygame.image.load(BACKGROUND_IMAGE)
background_img = pygame.transform.scale(background_img, (resolutionWidth, resolutionHeight))
background_position = (0, 0)
Font = pygame.font.Font(FONT_PATH, FONT_SIZE)
BUTTON_ACTION_MAP = {}

class Menu:
    """Defines what a menu is and does"""
    def __init__(self, x, y, width, height, name='unnamed', radius=0, parent_menu=None ) -> None:
        self.radius =radius
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height),pygame.SRCALPHA)
        self.transparency = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_displayed = False
        self.is_selected = False
        self.is_locked = False
        self.auto_hide = False
        self.is_button_list = False #list of buttons need to change this var name
        self.is_menu_list = False
        self.parent_menu:Menu = parent_menu if parent_menu != None else self
        #need to keep track of menus positioning on Canvas this is done by offseting the postion based on the parent menus positioning. 
        self.absolute_rect = pygame.Rect(self.x + self.parent_menu.x, self.y + self.parent_menu.y, self.width, self.height) if self.parent_menu != self else self.rect
        self.sub_menus: List[Menu] = []
        self.button_matrix:  List[List[Button]] = [[]]
        #creating dictionaries for easy refrence
        self.sub_menus_dict: dict = {}
        self.button_dict: dict = {}
        self.input_boxs_fields = []
        self.input_boxes: list[TextInput] = []
        self.text_window: TextWindow = TextWindow(self.x, self.y, self.width, self.height, self, messsage='NotSet', name='Default')#Creates a text window on menu if one exists
        self.button_action_map = {}
        #menu state fields assign addional variables based on states of menus
        self.last_button_selected = None 
        self.sub_menus_buttons_active: list[Button]= []
        #button to activate menu when selected 
        self.activate_button: Button = Button(0, 0, 0, 0, self)
    
    def display_text_window(self):
        self.text_window.display()
    def display_input_boxes(self):
        for input in self.input_boxes:
            input.display()
    def display_buttons(self):
        for button in self._get_all_buttons():
            button.display()
            self.last_button_selected = button if button.is_selected else self.last_button_selected
    def listener(self):
        """updates states"""
        self.sub_menus_buttons_active = self._update_submenus_selected_buttons()
        if self.activate_button.is_selected and self.parent_menu.is_locked == False:
            self.is_displayed = True
        elif self.auto_hide:
            self.is_displayed = False

    def display(self):
        """Displays all buttons text windows input boxs and buttons on menu"""
        self.listener()
        if self.is_displayed:
            if self.text_window.name != 'Default':
                self.text_window.display()
            if self.button_matrix:
                self.display_buttons()
            if self.input_boxes:
                self.display_input_boxes()
            if self.parent_menu == self:
                    Canvas.blit(self.surface, self.rect)
            else:
               #Canvas.blit(self.surface, self.rect)
               self.parent_menu.surface.blit(self.surface, self.rect )
            for submenu in self._get_all_submenus():
                submenu.display()
            #displays transparnet background
            if self.is_selected:
                transparency = self.transparency * 2
            else:
                transparency = self.transparency
            pygame.draw.rect(self.surface, (0,0,0,transparency), (0,0,self.width, self.height),border_radius=self.radius)
    
    def _get_total_buttons_count(self):
        """this is to determine how many rows"""
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
        #currently only returning the first button that shows selected, may need to adjust this
        idx = 0
        row = 0
        for array in self.button_matrix:
            for button in array:
                if button.is_selected:
                    row = self.button_matrix.index(array)
                    idx = array.index(button)
        return idx, row

    def _set_input_text_fields(self, text_width: int = 600, text_height: int = 40, start_x = 500, start_y =100) -> None:
        """Adds text fields vertiaclly(default) to menu"""
        spacing = 50 
        for idx, field in enumerate(self.input_boxs_fields):
            new_text_input = TextInput(start_x, start_y + idx * spacing,text_width, text_height, self, field)
            self.input_boxes.append(new_text_input)

    def _set_buttons(self,buttons:list[dict[str, str]], x_pos: float = 0, y_pos=0,button_width: int = 150, button_height: int = 40, horizontal_spacing: int = 150, font: pygame.font.Font = Font) -> None:
        """Adds buttons to menu"""
        set_buttons = []
        #if not list
        padding: int = 31
        max_width = self.width - 2 * padding
        buttons_per_row = max_width // (button_width + padding)
        total_buttons = len(buttons)
        rows = (total_buttons + buttons_per_row - 1) // buttons_per_row #Celing division 
        x_start = 50
        y_start = 10
        if rows > 0:
            self.button_matrix = [[] for _ in range(int(rows))]
        for idx, button in enumerate(buttons):
            button_name = button["name"]
            if not self.is_button_list:
                row = idx // buttons_per_row
                col = idx % buttons_per_row
                x = x_start + col * (button_width + padding)
                y = y_start + padding + row * (button_height + padding)
                new_button = Button(x,y,button_width,button_height, self,font, button_name)
                self.button_matrix[int(row)].append(new_button)
            else:
                new_button = Button(x_pos + x_start,y_pos + 50,button_width,button_height, self,font, button_name)
                set_buttons.append(new_button)
                x_pos += horizontal_spacing
                new_row: List[Button] = set_buttons
                if len(self.button_matrix[0]) == 0:
                     self.button_matrix[0] = new_row
                else:
                    self.button_matrix.append(new_row)
                
            if "image" in button:
                image = pygame.image.load(button["image"])
                new_button.image = pygame.transform.scale(image, (button_width, button_height))
                new_button.is_image = True

            self.button_dict[button_name] = new_button

    
    def _set_button_actions(self):
        """set the button actions based on a dict of methods"""
        for button_list in self.button_matrix:
            for button in button_list:
                if button.name in self.button_action_map:
                    button.action = self.button_action_map[button.name]

    def _get_all_submenus(self):
        """Returns a list all nested submenus."""
        menu_list: List[Menu] = []

        def collect_menus(menu: Menu) -> None:
            """Recursively collect all menus and their submenus."""
            menu_list.append(menu)  # Add the current menu
            for submenu in menu.sub_menus:  # Recurse into submenus
                collect_menus(submenu)

        # Iterate over top-level menus
        for menu in self.sub_menus:
            collect_menus(menu)
        
        return menu_list
    
    def _update_submenu_dict(self) -> None:
        """using this is for easy refrence of menus, but have not utilized yet"""
        for menu in self.sub_menus:
            self.sub_menus_dict[menu.name] = menu
            
    def _update_submenus_selected_buttons(self) -> List:
        """creates list of buttons on submenus that are currenlty in the selected state"""
        selected_buttons = []
        for menu in self._get_all_submenus():
            selected_buttons.append(menu.last_button_selected)
        return selected_buttons

    def _print_button_matrix(self):
        """adding a diagnostic method to look at the matrix"""
        #del when done
        for idx, row in enumerate(self.button_matrix):
            for button in row:
                print("row is: {idx} name: {button}".format(idx=idx, button=button.name))

class Button:
    def __init__(self, x, y, width, height, menu:Menu,font:pygame.font.Font=Font, name='unnamed' ):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font =font
        self.is_displayed = False
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.menu = menu
        self.menu_surface = menu.surface
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #Set Text Front if button is Text Only
        self.text = Text(self.x, self.y,menu, self.font, self.name)
        self.text.rect = self.rect
        self.background = True
        self.select_rectangle = False
        #Set Image if button is image
        self.is_image = False
        self.image = pygame.image.load(TEST_BUTTON_IMAGE)
        #the postion of the button on the canvas vs Surface
        self.absolute_rect = self._absolute_rect()
        self.is_selected = False
        
    def _absolute_rect(self):
        x_offset = self.x + self.menu.absolute_rect.x
        y_offset = self.y + self.menu.absolute_rect.y

        return pygame.Rect(x_offset,y_offset, self.width, self.height)
    def action(self):
        """define the action the button takes when clicked or enter is pressed"""
        print(self.name)

    def display_image(self):
        """display image of button"""
        padding = 5
        #draw background for Apps 
        if self.background: 
            pygame.draw.rect(self.menu_surface, (BUTTON_BG_COLOR), 
                             (self.rect.x - padding, 
                              self.rect.y - padding, 
                              self.image.get_width() + 2 * padding, 
                              self.image.get_height() + 2 * padding))
        
        if self.is_selected:
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
            if self.background:
                self.text.display_background()
            self.text.display()
        if self.is_selected:
            self.text.highlighted = True
        else:
            self.text.highlighted = False
    
        

class Text:
    """creates text for buttons"""
    def __init__(self, x, y,  menu:Menu, font:pygame.font.Font=Font, text="Default",background_x_offset=40, background_y_offset=20,) -> None:
        self.menu = menu
        self.x = x
        self.y = y
        self.font =font
        self.text = self.font.render(text, True, BLACK)
        self.text_highlighted = font.render(text, True, (255, 255, 255))
        self.width, self.height = font.size(text)
        self.text_surface  = pygame.Surface((self.width, self.height), pygame.SRCALPHA) 
        self.rect = pygame.Rect(x, y, self.width, self.height)
        #ADD BACKGROUND
        self.background_rect = pygame.Rect(x-10, y-10, self.width + background_x_offset, self.height + background_y_offset)
        self.highlighted = False
        self.background = False

    def display_background(self):
        """"Displays background"""
        pygame.draw.rect(self.menu.surface, (255,255,255,90),(self.x - 30,self.y -10,self.width *2,self.height * 2), border_radius=RADIUS)
    def display_text(self):
        """hightlight text when selected"""
        self.menu.surface.blit(self.text, self.rect)
    def display_highlighted(self):
        self.menu.surface.blit(self.text_highlighted, self.rect)
    def display(self):
        if self.background:
            self.display_background()        
        if self.highlighted:
            self.display_highlighted()
        else:
            self.display_text()


class TextInput:
    """creates a field for user to input text"""
    def __init__(self, x, y, width, height, menu:Menu, name="TextInput") -> None:
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

class TextWindow:
    """creates in window on the surface that displays a message """
    def __init__(self, x, y, width, height, menu:Menu, messsage, name="TextWindow") -> None:
        self.name = name
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.menu = menu
        self.message = messsage
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.font = pygame.font.SysFont("Roboto", 31) 

    def wrap_text(self, message):
        """Wrap text to fit within max_width on a surface."""
        words = message.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            text_surface = self.font.render(test_line, True, (0, 0, 0))
            if text_surface.get_width() <= self.width -10:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines


    def display(self):
        """Display the message window""" 
        self.message = str(self.message) if self.message is not None else "Unknown error"
        self.surface.fill((0,0,0,100))
        text_y = 10
        for line in self.wrap_text(self.message):
            text_surface = self.font.render(line, True, WHITE)
            self.surface.blit(text_surface, (10,text_y))
            text_y += 30
        Canvas.blit(self.surface, (self.x, self.y))



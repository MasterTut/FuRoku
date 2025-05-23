
import json
from components import * 

def setup_side_menu() -> Menu:
    """intialize SideMenu"""
    side_menu = Menu(0, 0,Canvas.get_width(), Canvas.get_height(), name="side_menu")
    side_menu.is_button_list = True
    side_menu.is_active = True
    button_width: int = 150 
    button_height: int = 40 
    vertical_spacing: int = 50
    y_offset = 90
    x_pos = 50
    for button_text in read_file():
           #Change option for Settings
           if button_text == "SETTINGS":
               y_pos = (side_menu.height * .9)
               button = Button(x_pos + 35, y_pos, button_width, button_height, side_menu, name=button_text)
               button.background = False
               button.image = pygame.image.load(SETTINGS_GEAR)
               button.is_image = True
               
           else:
               button = Button(x_pos, y_offset, button_width, button_height, side_menu, name=button_text)
               button.select_rectangle = True
               button.background =False
           side_menu.button_matrix[0].append(button)
           y_offset += vertical_spacing

    return side_menu

def import_app_customization_menus() -> Menu:
    """initalize App Customization Menu"""
    #need to change 107 in manager
    submenu_names = ["action_select", "menu_select" ]
    x_pos = int(Canvas.get_width() * .15)
    width = int(Canvas.get_width() - (x_pos +50))
    add_remove_edit = Menu(x_pos, 0, width, Canvas.get_height(), "add_remove_edit")
    add_remove_edit.transparency = 10
    add_remove_edit.is_menu_list = True
    buttons =[[{"name": "ADD"}, {"name": "EDIT"}, {"name": "REMOVE"}], [{"name": "APPS"}, {"name": "GAMES"}]]
    font = pygame.font.SysFont("Robto", 31)
    button_idx = 0
    vertical_pos = 10
    for menu_name in submenu_names:
        menu = Menu(40, vertical_pos, Canvas.get_width() -400, 150, menu_name, 20, parent_menu=add_remove_edit)
        menu._set_buttons(buttons[button_idx], font=font)
        menu.transparency = 30
        vertical_pos += 200
        button_idx += 1
        menu.parent_menu = add_remove_edit
        add_remove_edit.sub_menus.append(menu)
    

    return add_remove_edit

def _import_apps_to_settings_menu(menu_manager):
    """"Import menus to display for buttons on settings menu"""
    menu = menu_manager.side_menu.sub_menus[-1]
    for submenu in menu.sub_menus:
        def _activate_menu():
            menu_manager._selected_menu = submenu
            submenu.is_active = True
            menu_manager._selected_menu = menu_manager._selected_menu.sub_menus[0]
            menu_manager.side_menu.is_locked = True
            for menu in submenu._get_all_submenus():
                menu.is_active = True
        for button in menu._get_all_buttons():
            if button.name ==  submenu.name:
                button.action = _activate_menu 

   
def import_apps(menu_name, apps_list) -> Menu:
       """Import Menus and Image Buttons from json example: Apps { Name: Netflix, CMD: chromium..."""
       x_pos = int(Canvas.get_width() * .15)
       width = int(Canvas.get_width() - (x_pos +50))
       
       new_menu = Menu(x_pos, 0, width, Canvas.get_height(), menu_name)
       new_menu._set_buttons(apps_list, button_width=256, button_height=256)
       return new_menu
   
def read_file():
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
           import_apps(menu_name, data[menu_name]) 
       return custom_menu_names


def _Submit_button_action(self):
        dataFromTextInput = {'name': '', 'image': '', 'cmd': ''}
        self.menuFromInput = self.menu.input_boxes[0].text
        for input in self.menu.input_boxes[1:]:
            dataFromTextInput[input.name] = input.text
        with open (APPS_PATH, 'r') as file:
            dataFromFile = json.load(file)
        if self.menuFromInput in dataFromFile:
            dataFromFile[self.menu.input_boxes[0].text].append(dataFromTextInput) 
        else:
            dataFromFile[self.menu.input_boxes[0].text] = [dataFromTextInput]
        if os.path.exists(dataFromTextInput['image']):
            with open (APPS_PATH, 'w') as file:
                json.dump(dataFromFile, file, indent =4)
            print('Write Complete')
        else:
            print("ERROR")
            #self.menu.errorWindow.message = "No Such file"
            #self.menu.errorWindow.error = True
    
def _CANCEL_button_action(self):
        self.menu.is_locked = False
        self.menu.is_active =False

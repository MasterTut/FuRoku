
import json
from components import * 


def read_file()-> Dict:
       """reads apps.json and send to import apps"""
       #check if file exists otherwise create a default one
       if not os.path.exists(APPS_PATH):
           print("apps.json not found, creating a default file.")
           default_data = {"apps": [{"name": "defaultApp", "image": "./Assets/defaultApp.png" }]}
           with open(APPS_PATH, 'w') as f:
               json.dump(default_data, f, indent=2)

       with open(APPS_PATH, 'r') as apps:
           data = json.load(apps)
       return data

def import_apps(menu_name, apps_list,width,x_pos,y_pos,parent_menu, button_dementions: int = 256) -> Menu:
       """Import Menus and Image Buttons from json example: Apps { Name: Netflix, CMD: chromium..."""
       new_menu = Menu(x_pos, y_pos, width, Canvas.get_height(), menu_name, parent_menu=parent_menu)
       new_menu._set_buttons(apps_list, button_width=button_dementions, button_height=button_dementions)

       return new_menu

CUSTOM_MENU_DATA = read_file()

def setup_side_menu(manager) -> Menu:
    """intialize SideMenu"""
    side_menu = Menu(0, 0,Canvas.get_width(), Canvas.get_height(), name="side_menu")
    side_menu.is_button_list = True
    side_menu.is_displayed = True
    button_width: int = 150 
    button_height: int = 40 
    vertical_spacing: int = 50
    y_offset = 90
    x_pos = 50
    
    #Create custom submenus for Side_Menu by reading a .json
    for menu_name in CUSTOM_MENU_DATA:
        
        x_pos_sub_menu = int(Canvas.get_width() * .15)
        width = int(Canvas.get_width() - (x_pos_sub_menu +50))
        new_menu = import_apps(menu_name, CUSTOM_MENU_DATA[menu_name], width, x_pos_sub_menu, y_pos=0, parent_menu=side_menu)
        side_menu.sub_menus.append(new_menu)

        for button in CUSTOM_MENU_DATA[menu_name]:
            if "url" in button:
                param = ' --start-fullscreen --kiosk --user-agent="Roku/DVP-12.0"'
                url = button['url']  
                def action():
                    webbrowser.open(url) 
                new_menu.button_action_map[button['name']] = action 
        new_menu._set_button_actions()

    settings_menu = None
    for menu in side_menu.sub_menus:
           #Setup Settings Menu
           if menu.name == "SETTINGS":
               y_pos = (side_menu.height * .9)
               button = Button(x_pos + 35, y_pos, button_width, button_height, side_menu, name=menu.name)
               menu.activate_button = button
               button.background = False
               button.image = pygame.image.load(SETTINGS_GEAR)
               button.is_image = True
               settings_menu = menu 
               settings_menu.sub_menus.append(setup_app_customization_menu(manager))
           else:
           #Add the rest of the text buttons on the side menu
               button = Button(x_pos, y_offset, button_width, button_height, side_menu, name=menu.name)
               menu.activate_button = button
               button.select_rectangle = True
               button.background =False
           side_menu.button_matrix[0].append(button)
           y_offset += vertical_spacing
    
    #Setting APPs Actions to active Menus on sideMenu
    if settings_menu:
        for submenu in settings_menu.sub_menus:
            print(submenu.name)
            def _activate_menu():
                manager._selected_menu = submenu
                print('true')
                submenu.is_displayed = True
                manager._selected_menu = manager._selected_menu.sub_menus[0]
                manager.side_menu.is_locked = True
                settings_menu.is_locked = True
                settings_menu.is_displayed = False
                for menu in submenu.sub_menus:
                    if menu.name not in CUSTOM_MENU_DATA:
                        menu.is_displayed = True
            for button in settings_menu._get_all_buttons():
                if button.name ==  submenu.name:
                    button.action = _activate_menu
    
    side_menu._update_submenu_dict()
    return side_menu

def setup_app_customization_menu(manager) -> Menu:
    """initalize App Customization Menu"""
    #Setup Parent Menu
    x_pos = int(Canvas.get_width() * .15)
    width = int(Canvas.get_width() - (x_pos +50))
    app_customization_menu = Menu(x_pos, 0, width, Canvas.get_height(), "add_remove_edit")
    app_customization_menu.transparency = 10
    app_customization_menu.is_menu_list = True
    #Mapping Actions of buttons for submenus
    def _CANCEL():
        manager.side_menu.is_locked = False
        manager.side_menu.sub_menus_dict['SETTINGS'].is_locked = False
        manager.side_menu.sub_menus_dict['SETTINGS'].is_displayed = True
    def _ADD():
        pass
    def _APP_ACTION():
        button = manager._selected_button.name
        menu: Menu= manager._selected_menu.name
        action = next((button.name for button in app_customization_menu.sub_menus_buttons_active if button.menu.name == 'action_select'))
        if action == 'REMOVE':
            print('REMOVE')
            CUSTOM_MENU_DATA[menu] = [app for app in CUSTOM_MENU_DATA[menu] if app["name"] != button]
        if action == 'EDIT':
            print('EDIT')
        else:
            print(action)
    
    button_action_map = {}
    button_action_map['CANCEL'] = _CANCEL
    button_action_map['ADD'] = _ADD
    #Setting up Sub_menus
    #Assigning every menu the button action map, this means there can be no duplicate button names action select menu
    vertical_pos = 10
    submenu_names = ["action_select","menu_select",  "submit_cancel"]
    action_buttons = [{"name": "ADD"}, {"name": "EDIT"}, {"name": "REMOVE"}]
    menu_select_buttons = [{"name": key} for key in CUSTOM_MENU_DATA if key != 'SETTINGS']
    submit_cancel_buttons= [{"name": "SUBMIT"}, {"name": "CANCEL"}]
    font = pygame.font.SysFont("Robto", 31)
    for menu_name in submenu_names:
        menu = Menu(40, vertical_pos, Canvas.get_width() -400, 150, menu_name, 20, parent_menu=app_customization_menu)
        if menu.name == 'action_select':
            menu._set_buttons(action_buttons, font=font)
        if menu.name == 'menu_select':
            menu._set_buttons(menu_select_buttons, font=font)
        if menu_name == 'submit_cancel':
            menu._set_buttons(submit_cancel_buttons, font=font)
        menu.button_action_map = button_action_map
        menu._set_button_actions()
        menu.transparency = 30
        vertical_pos += 200

        app_customization_menu.sub_menus.append(menu)
    app_customization_menu._update_submenu_dict()

    #add another menu for displaying apps on customization menu 
    for menu_name in CUSTOM_MENU_DATA:
        if menu_name != "SETTINGS":
            width = int(Canvas.get_width() -400)
            new_menu = import_apps(menu_name, CUSTOM_MENU_DATA[menu_name], width, 40, y_pos=vertical_pos,button_dementions =48, parent_menu=app_customization_menu)
            new_menu.activate_button = app_customization_menu.sub_menus_dict['menu_select'].button_dict[menu_name]
            new_menu.auto_hide = True
            new_menu.transparency = 30
            #new_menu.parent_menu = app_customization_menu
            app_customization_menu.sub_menus.append(new_menu)
            #setting the buttons dynamicly depending on what button is selected 
            for button_list in new_menu.button_matrix:
                for button in button_list:
                        button.action = _APP_ACTION 
    
    app_customization_menu._update_submenu_dict()
    return app_customization_menu


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

    

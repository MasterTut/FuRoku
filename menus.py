
import json
from components import * 


def import_menus():
    """Create a bunch of menus"""
    #need to change 107 in manager
    submenu_names = ["action_select", "menu_select" ]
    x_pos = int(Canvas.get_width() * .15)
    width = int(Canvas.get_width() - (x_pos +50))
    add_remove_edit = Menu(x_pos, 0, width, Canvas.get_height(), "add_remove_edit")
    add_remove_edit.transparency = 10
    add_remove_edit.is_menu_list = True
    add_remove_edit.is_list = False
    buttons =[[{"name": "ADD"}, {"name": "EDIT"}, {"name": "REMOVE"}], [{"name": "APPS"}, {"name": "GAMES"}]]
    font = pygame.font.SysFont("Robto", 31)
    button_idx = 0
    vertical_pos = 10
    for menu_name in submenu_names:
        menu = Menu(40, vertical_pos, Canvas.get_width() -400, 150, menu_name, 20, parent_menu=add_remove_edit)
        menu.is_list = False
        menu._set_buttons(buttons[button_idx], font=font)
        menu.transparency = 30
        vertical_pos += 200
        button_idx += 1
        menu.parent_menu = add_remove_edit
        add_remove_edit.sub_menus.append(menu)
    

    return add_remove_edit



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

#!/usr/bin/python3
from manager import *

#setup
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()

manager = Manager()


#Creates the game loop to update the screen
def update_display():
    while True:
        Canvas.blit(background_img, dest = background_position) 
        manager.menu_mgr._display_menus()
        manager.listener()
        clock.tick(FPS)
        pygame.display.update()

#Initalize and run
if __name__ == "__main__":
    update_display()
    pygame.quit()

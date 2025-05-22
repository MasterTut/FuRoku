#!/usr/bin/python3
from manager import *

#setup
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()

manager = Manager()


#Creates the game loop to update the screen
def update_display():
    while True:
        #background_surface = pygame.Surface((Canvas.get_width(), Canvas.get_height()), pygame.SRCALPHA)
        #pygame.draw.rect(background_surface, (30,30,90), (0,0,Canvas.get_width(),Canvas.get_height()))
        #Canvas.blit(background_surface,background_position)
        Canvas.blit(background_img, dest = background_position) 
        manager.menu_mgr._display_menus()
        manager.listener()
        clock.tick(FPS)
        pygame.display.update()

#Initalize and run
if __name__ == "__main__":
    update_display()
    pygame.quit()

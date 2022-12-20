from display.title_screen_menu import Title_screen_menu
import pygame

class Title_screen():
    def __init__(self, window: pygame.Surface) -> None:
        self.ui = Title_screen_menu(window)

        self.clock = pygame.time.Clock()
    
    def run(self) -> bool:
        # variable permettant de faire fonctionner la boucle de jeu.
        # Initialisation des variables...
        dt = self.clock.tick(0) / 1000
        while True:
            for event in pygame.event.get():
                # pour fermer avec la croix
                if event.type == pygame.QUIT:
                    # on ferme sans lancer le jeu
                    return False
                self.ui.event_handler(event)
            
            

            if self.ui.must_start_game():
                return True
            
            self.ui.update()
            self.ui.draw()

            dt = self.clock.tick(0) / 1000
            
            pygame.display.update()
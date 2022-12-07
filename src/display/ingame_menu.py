from display.ui import UI, Label, Button, Progressbar
import pygame
class Ingame_menu(UI):
    def __init__(self, draw_surface):
        super().__init__(draw_surface)

        self.font = pygame.font.Font("../graphics/PublicPixel.ttf", 20)
        self.firstlabel  = Label(pygame.Vector2(0, 0), "test", self.font, pygame.Color(255, 255, 255))
        self.firstbutton = Button( pygame.Rect(50, 50, 150, 40), "Bouton", self.font, self.delete_button, pygame.Color(255, 255, 255), pygame.Color(127, 127, 127), hover_color= pygame.Color(50, 50, 50))
        progressbar_rect = pygame.Rect((0, 0, 0, 0))
        progressbar_rect.x = 10
        progressbar_rect.y = draw_surface.get_height() - 25
        progressbar_rect.width = draw_surface.get_width()-20
        progressbar_rect.height = 15

        self.fightprogressbar = Progressbar(progressbar_rect, 0, 100, pygame.Color(85, 160, 39), pygame.Color(134, 221, 81))

        self.bind_widget(self.firstlabel)
        self.bind_widget(self.firstbutton)
        self.bind_widget(self.fightprogressbar)

    def delete_button(self):
        self.unbind_widget(self.firstbutton)

    def update(self, fps:float | None = None, distance:int | None= None):
        super().update()
        
        if fps != None:
            self.firstlabel.update_text(f"{fps:.2f}")
        
        if distance != None:
            self.fightprogressbar.update_value((self.fightprogressbar.value+distance)%100)
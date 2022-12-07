from display.ui import UI, Label, Button, Progressbar
import pygame
class Ingame_menu(UI):
    def __init__(self, draw_surface):
        super().__init__(draw_surface)

        self.font_15 = pygame.font.Font("../graphics/PublicPixel.ttf", 15)
        self.font_20 = pygame.font.Font("../graphics/PublicPixel.ttf", 20)
        
        self.firstlabel  = Label(pygame.Vector2(10, 10), "", self.font_15, pygame.Color(255, 255, 255))
        
        button_rect = pygame.Rect((0,20,100,40))
        button_rect.x = draw_surface.get_width() - button_rect.width - 20
        
        self.firstbutton = Button(button_rect, "Menu", self.font_20, self.delete_button, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        
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
            self.firstlabel.update_text(f"fps: {fps:.2f}")
        
        if distance != None:
            self.fightprogressbar.update_value((self.fightprogressbar.value+distance)%100)
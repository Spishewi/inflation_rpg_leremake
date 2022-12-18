from __future__ import annotations

import pygame
import math
import typing
from utils import DynamicImage

class Default_font(pygame.font.Font):
    def __init__(self,size):
        super().__init__("../graphics/PublicPixel.ttf",size)


class Widget():
    def __init__(self) -> None:
        pass
    def draw(self, display_surface: pygame.Surface) -> None:
        pass
    def update(self) -> None:
        pass
    def event_handler(self, event: pygame.event.Event) -> None:
        pass
class Progressbar(Widget):
    def __init__(self, rect: pygame.Rect, value: int | float, max_value: int | float, color: pygame.Color, outline_color: pygame.Color) -> None:

        self.rect = rect
        self.color = color
        self.outline_color = outline_color

        self.value = value
        self.max_value = max_value

    def draw(self, draw_surface: pygame.Surface) -> None:
        progressbar_outline = self.rect
        progressbar_width = math.floor((self.value/self.max_value) * (progressbar_outline.width - 4))
        progressbar_innerbar = pygame.Rect(progressbar_outline.x + 2, progressbar_outline.y + 2, progressbar_width, progressbar_outline.height - 4)

        pygame.draw.rect(draw_surface, self.outline_color, progressbar_outline, 1)
        pygame.draw.rect(draw_surface, self.color, progressbar_innerbar)

    def update_value(self, value: int | float) -> None:
        self.value = min(value, self.max_value)

class Label(Widget):
    def __init__(self, coords: pygame.Vector2, text: str, font: pygame.font.Font, text_color: pygame.Color) -> None:
        self.coords = coords
        self.text_color = text_color
        self.font = font
        
        self.text = None
        self._rendered_text = None
        self.update_text(text)

    def update_text(self, text):
        self.text = text
        self._rendered_text = self.font.render(self.text, False, self.text_color)

    def draw(self, draw_surface: pygame.Surface) -> None:
        draw_surface.blit(self._rendered_text, self.coords)

class Button(Widget):
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font, callback: typing.Callable, text_color: pygame.Color, color: pygame.Color, hover_text_color: pygame.Color = None, hover_color: pygame.Color = None):
        self.text = text
        self.rect = rect
        self.color = color
        self.text_color = text_color
        self.font = font

        if hover_color != None:
            self.hover_color = hover_color
        else:
            self.hover_color = self.color

        if hover_text_color != None:
            self.hover_text_color = hover_text_color
        else:
            self.hover_text_color = self.text_color

        self.callback = callback

        self.rendered_text = None
        self.rendered_text_hovered = None

        self.hovered = False
        self.clicked = False
    
    def update(self) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self, draw_surface: pygame.Surface) -> None:
        rect_surface = pygame.Surface(self.rect.size)
        

        if self.hovered:
            if self.rendered_text_hovered == None:
                self.rendered_text_hovered = self.font.render(self.text, False, self.hover_text_color)
            
            pos = pygame.Vector2()
            pos.x = (rect_surface.get_width() - self.rendered_text_hovered.get_width()) // 2
            pos.y = (rect_surface.get_height() - self.rendered_text_hovered.get_height()) // 2

            rect_surface.fill(self.hover_color)
            rect_surface.blit(self.rendered_text_hovered, pos)
        else:
            if self.rendered_text == None:
                self.rendered_text = self.font.render(self.text, False, self.text_color)

            pos = pygame.Vector2()
            pos.x = (rect_surface.get_width() - self.rendered_text.get_width()) // 2
            pos.y = (rect_surface.get_height() - self.rendered_text.get_height()) // 2

            rect_surface.fill(self.color)
            rect_surface.blit(self.rendered_text, pos)

        draw_surface.blit(rect_surface, self.rect.topleft)

    def event_handler(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked:
                self.clicked = False
                self.callback()
                
class Image(DynamicImage):
    def __init__(self, path:str, zoom:int, pos:pygame.Vector2):
        image = pygame.image.load(path)
        self.pos = pos
        self.zoom = zoom
        super().__init__(image,False)
    
    def draw(self, draw_surface : pygame.Surface):
        draw_surface.blit(self.get_image(self.zoom),self.pos)
        
    def event_handler(self, event) -> None:
        return
    def update(self) -> None:
        return
        

Widget = typing.Union[Button, Progressbar, Label]

class UI():
    def __init__(self, draw_surface: pygame.Surface) -> None:
        self.draw_surface = draw_surface
        self.widgets: list[Widget] = []
        self.background = None
        self.need_grab = False

    def event_handler(self, event: pygame.event.Event):
        for widget in self.widgets:
            widget.event_handler(event)

    def update(self):
        for widget in self.widgets:
            widget.update()

    def draw(self):
        if self.background != None:
            background_surface  = pygame.Surface(self.draw_surface.get_size())
            background_surface.fill(self.background)
            background_surface.set_alpha(self.background.a)
            self.draw_surface.blit(background_surface, (0, 0))
        
        for widget in self.widgets:
            widget.draw(self.draw_surface)

    def bind_widget(self, widget: Widget):
        if not issubclass(type(widget), Widget):
                raise ValueError
        if widget not in self.widgets:
            self.widgets.append(widget)

    def bind_several_widget(self, *args):
        for widget in args:
            if not issubclass(type(widget), Widget):
                raise ValueError

            self.bind_widget(widget)

    def unbind_widget(self, widget: Widget):
        if not issubclass(type(widget), Widget):
                raise ValueError
        if widget in self.widgets:
            self.widgets.remove(widget)
    
    def clear_widget(self):
        self.widgets = []

    def set_background_color(self, color: pygame.Color | None):
        if not (isinstance(color, pygame.Color) or isinstance(color, type(None))):
            raise ValueError
        self.background = color

    def set_grab(self, value: bool):
        self.need_grab = value

    def get_grab(self) -> bool:
        return self.need_grab
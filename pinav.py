import pygame
from math import floor, ceil, sqrt

pygame.init()
pygame.font.init()

class Menu():
    padding = 20

    def __init__(self, surface=None, buttons=[]):
        self.surface = surface
        self.buttons = buttons
        self.rows = 0
        self.cols = 0
        self.buttonH = 0
        self.buttonW = 0
        self.buttonMap = []

    def add(self, button):
        self.buttons.append(button)
        self.render()

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
                button = self.buttonAt(pygame.mouse.get_pos())
                if button:
                    if button.action:
                        button.action()
                    else:
                        print(button.label)
    
    def buttonAt(self, pos):

        for rect, button in self.buttonMap:
                if rect.collidepoint(pos):
                        return button
        return None

    def render(self):
        if self.surface:
            self.buttonMap = []

            self.surface.fill((0,0,0))

            self.rows = floor(sqrt(len(self.buttons)))
            self.cols = ceil(len(self.buttons)/self.rows)

            self.buttonW = self.surface.get_width() // self.cols - self.padding;
            self.buttonH = self.surface.get_height() // self.rows - self.padding;
    
            for index, button in enumerate(self.buttons):

                button.render((self.buttonW, self.buttonH))
                col = index % self.cols
                row = index // self.cols

                x = col * (self.buttonW + self.padding) + self.padding // 2
                y = row * (self.buttonH + self.padding) + self.padding // 2
                w = self.buttonW
                h = self.buttonH

                rect = pygame.Rect(x,y,w,h)

                self.surface.blit(button.surface, rect)

                self.buttonMap.append((rect, button))


class Button():
    font = pygame.font.SysFont(None, 48)
    padding = 20

    def __init__(self, label="", icon=None, bgColor=(255,255,255), fgColor=(0,0,0), action = None):
        self.label = label
        self.icon = icon
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.surface = pygame.Surface((0,0))
        self.rect = pygame.Rect(0,0,0,0)
        self.action = action

    def render(self, size):
        if size != self.surface.get_size():
            # initialize surface
            self.surface = pygame.Surface(size)
            self.surface.fill(self.bgColor)

            # render label
            fontSurf = self.font.render(self.label, True, self.fgColor, self.bgColor)
            fontX = (self.surface.get_width() - fontSurf.get_width()) // 2
            fontY = (self.surface.get_height() - fontSurf.get_height()) // 2

            if self.icon:
                    fontY += (self.padding + self.icon.get_height()) // 2

            fontRect = pygame.Rect((fontX, fontY), fontSurf.get_size())
            self.surface.blit(fontSurf, fontRect)

            # render icon
            if not self.icon:
                    return

            iconX = (self.surface.get_width() - self.icon.get_width()) // 2
            iconY = (self.surface.get_height() - self.icon.get_height()) // 2

            if self.label:
                    iconY -= (self.padding + fontSurf.get_height()) // 2

            iconRect = pygame.Rect((iconX, iconY), self.icon.get_size())
            self.surface.blit(self.icon, iconRect)

def loadIcon(path):
    pass

def main():
    screen = pygame.display.set_mode((1366,768), flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

    menu = Menu(screen)
    menu.add(Button(label='foo', bgColor=(0,255,0), icon=pygame.image.load('alert.gif')))
    menu.add(Button(label='quit', bgColor=(0,0,255), action=pygame.quit))
    pygame.display.update()
    while(True):
        for event in pygame.event.get():
            menu.handleEvent(event)
            if event.type == pygame.QUIT:
                pygame.quit()

if __name__ == "__main__":
        main()

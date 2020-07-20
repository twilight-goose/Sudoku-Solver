import pygame
pygame.init()


class Button:
    """ Simple button class that is not much more than a text in a box"""
    font = pygame.font.SysFont("Arial", 20)

    def __init__(self, text, pos, colour=(255, 255, 255)):
        self.image = pygame.Surface((150, 50))
        self.image.fill((120, 120, 120))
        self.x_range = (pos[0], pos[0] + 300)
        self.y_range = (pos[1], pos[1] + 100)
        self.text = self.font.render(text, True, colour)
        self.colour = colour
        self.image.blit(self.text, ((self.image.get_width() - self.text.get_width()) // 2,
                                    (self.image.get_height() - self.text.get_height()) // 2))
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def cannot_solve(self):
        self.image.fill((120, 120, 120))
        text2 = self.font.render("Cannot be solved", True, self.colour)
        self.image.blit(text2, ((self.image.get_width() - text2.get_width()) // 2,
                                    (self.image.get_height() - text2.get_height()) // 2))

    def reset(self):
        self.image.fill((120, 120, 120))
        self.image.blit(self.text, ((self.image.get_width() - self.text.get_width()) // 2,
                                    (self.image.get_height() - self.text.get_height()) // 2))


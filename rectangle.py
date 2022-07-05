import pygame


class RectangleLite:
    horizontal_padding = 5
    vertical_padding = 5

    def __init__(self, pos, width, height, centered_x=True, centered_y=True,
                 filled=True, fill_colour=(255, 255, 255, 255),
                 outlined=True, outline_colour=(0, 0, 0, 255), outline_thickness=2, outline_radius=0):
        x, y = pos
        self.position = pygame.Vector2(x, y)
        self.width = width
        self.height = height

        self.centered_x = centered_x
        self.centered_y = centered_y
        self.centering = pygame.Vector2(0, 0)

        self.filled = filled
        self.fill_colour = fill_colour

        self.outlined = outlined
        self.outline_colour = outline_colour
        self.outline_thickness = outline_thickness
        self.outline_radius = outline_radius

    def update(self, delta, x=None, y=None, width=None, height=None, fill_colour=None):
        if x is not None:
            self.position.x = x
        if y is not None:
            self.position.y = y
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if fill_colour is not None:
            self.fill_colour = fill_colour

        if self.centered_x:
            self.centering.x = self.width / 2
        if self.centered_y:
            self.centering.y = self.height / 2

    def get_collision_rect(self):
        return pygame.Rect(
            self.position - pygame.Vector2(self.horizontal_padding, self.vertical_padding) - self.centering,
            (self.width + 2 * self.horizontal_padding, self.height + 2 * self.vertical_padding))

    def draw(self, surface):
        r = self.get_collision_rect()
        if self.filled:
            pygame.draw.rect(surface, self.fill_colour, r,border_radius=self.outline_radius)
        if self.outlined:
            pygame.draw.rect(surface, self.outline_colour, r, self.outline_thickness, self.outline_radius)


class Rectangle(RectangleLite):

    def __init__(self, pos, width, height, centered_x=True, centered_y=True,
                 filled=True, fill_colour=(255, 255, 255, 255),
                 outlined=True, outline_colour=(0, 0, 0, 255), outline_thickness=2, outline_radius=0,
                 horizontal_padding=12, vertical_padding=12):

        super().__init__(pos, width, height, centered_x, centered_y, filled, fill_colour,
                         outlined, outline_colour, outline_thickness, outline_radius)

        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding

    def update(self, delta, x=None, y=None, dx=0, dy=0, width=None, height=None, fill_colour=None,
               centered_x=None, centered_y=None, outlined=None, outline_colour=None, outline_thickness=None,
               outline_radius=None):
        if x is not None:
            self.position.x = x
        if y is not None:
            self.position.y = y
        self.position += delta * pygame.Vector2(dx, dy)
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if fill_colour is not None:
            self.fill_colour = fill_colour
        if centered_x is not None:
            self.centered_x = centered_x
        if centered_y is not None:
            self.centered_y = centered_y
        if outlined is not None:
            self.outlined = outlined
        if self.outlined:
            if outline_colour is not None:
                self.outline_colour = outline_colour
            if outline_thickness is not None:
                self.outline_thickness = outline_thickness
            if outline_radius is not None:
                self.outline_radius = outline_radius

        if self.centered_x:
            self.centering.x = self.width / 2
        if self.centered_y:
            self.centering.y = self.height / 2

    def draw(self, surface):
        s = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        super().draw(s)
        surface.blit(s, (0, 0))

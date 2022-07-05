import pygame
from rectangle import RectangleLite, Rectangle


class LabelLite:
    horizontal_padding = 5
    vertical_padding = 5
    outline_thickness = 2

    def __init__(self, pos, text, font_size, text_colour=(0, 0, 0), antialias=True, centered_x=True, centered_y=True,
                 filled=False, fill_colour=(150, 150, 150), outlined=False, outline_colour=(0, 0, 0), outline_radius=2,
                 font_file="MontserratBlack-ZVK6J.otf"
                 ):
        self.position = pygame.Vector2(pos)

        self.centered_x = centered_x
        self.centered_y = centered_y
        self.centering = pygame.Vector2(0, 0)

        self.font_file = font_file
        self.font = pygame.font.Font(self.font_file, font_size)
        self.text_colour = text_colour
        self.antialias = antialias
        self.raw_text = text
        self.text, self.width, self.height = self.create_text(self.raw_text)

        self.rect = RectangleLite(pos, self.width, self.height, centered_x, centered_y, filled, fill_colour, outlined,
                                  outline_colour, self.outline_thickness, outline_radius)

        self.filled = filled
        self.fill_colour = fill_colour

        self.outlined = outlined
        self.outline_colour = outline_colour

    def create_text(self, text):
        out = []
        max_width = 0
        max_height = 0

        for line in text:
            text_surface = self.font.render(line, self.antialias, self.text_colour)
            width = text_surface.get_width()
            height = text_surface.get_height()
            out.append((text_surface, width, height))
            max_width = max(max_width, width)
            max_height += height
        return out, max_width, max_height

    def update(self, delta, new_text=None, x=None, y=None, width=None, height=None, colour=None, font_size=None):
        self.text, self.width, self.height = self.create_text(self.raw_text)

        if new_text is not None:
            self.text, self.width, self.height = self.create_text(new_text)
        if font_size is not None:
            self.font = pygame.font.Font(self.font_file, font_size)
            if new_text is not None:
                self.text, self.width, self.height = self.create_text(new_text)
            else:
                self.text, self.width, self.height = self.create_text(self.raw_text)

        if x is not None:
            self.position.x = x
        if y is not None:
            self.position.y = y
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if colour is not None:
            self.fill_colour = colour
        if self.centered_x:
            self.centering.x = self.width / 2
        if self.centered_y:
            self.centering.y = self.height / 2

        self.rect.update(delta, self.position.x, self.position.y, self.width, self.height, self.fill_colour)

    def draw(self, surface):

        self.rect.draw(surface)

        prev_height = 0
        for line in self.text:
            text_surface, width, height = line
            center = pygame.Vector2(0, 0)
            if self.centered_x:
                center.x = width / 2
            if self.centered_y:
                center.y = height / 2
            surface.blit(text_surface, self.position - center + pygame.Vector2(0, prev_height))
            prev_height += height


class Label:
    horizontal_padding = 5
    vertical_padding = 5
    outline_thickness = 3

    def __init__(self, pos, text, font_size, text_colour=(0, 0, 0), antialias=True, centered_x=True, centered_y=True,
                 filled=False, fill_colour=(150, 150, 150), outlined=False, outline_colour=(0, 0, 0), outline_radius=2,
                 font_file="MontserratBlack-ZVK6J.otf",
                 path=None, add_to_list=None):

        if path is None:
            path = globals()
        self.position = pygame.Vector2(pos)
        self.offset = pygame.Vector2(0, 0)

        self.centered_x = centered_x
        self.centered_y = centered_y
        self.centering = pygame.Vector2(0, 0)

        self.font_file = font_file
        self.font = pygame.font.Font(self.font_file, font_size)
        self.text_colour = text_colour
        self.antialias = antialias
        self.raw_text = text

        self.path = path
        self.text, self.width, self.height = self.create_text(self.raw_text, self.path)

        self.rect = RectangleLite(pos, self.width, self.height, centered_x, centered_y, filled, fill_colour, outlined,
                                  outline_colour, self.outline_thickness, outline_radius)

        self.filled = filled
        self.fill_colour = fill_colour

        self.outlined = outlined
        self.outline_colour = outline_colour

        if add_to_list is not None:
            if isinstance(add_to_list, list):
                add_to_list.append(self)
            elif isinstance(add_to_list, set):
                add_to_list.add(self)

    def create_text(self, text, path):
        """
        [["string ", [f"{var=}", path]], ["string2"]]
        string var
        string2
        """
        out = []
        max_width = 0
        max_height = 0

        for l in text:
            line = ""
            for thing in l:
                if isinstance(thing, list):
                    if len(thing) == 1:
                        value = thing[0].split('=')[0]
                        line += str(path[value])
                    else:
                        val, path = thing
                        value = val.split('=')[0]
                        if "self." in value:
                            ind = value.index("self.")
                            value = value[ind + 5:]
                        line += eval("str(path.%s)" % value)

                else:
                    line += thing

            text_surface = self.font.render(line, self.antialias, self.text_colour)
            width = text_surface.get_width()
            height = text_surface.get_height()
            out.append((text_surface, width, height))
            max_width = max(max_width, width)
            max_height += height
        return out, max_width, max_height

    def update(self, delta, new_text=None, x=None, y=None, width=None, height=None, colour=None, font_size=None,
               fill_colour=None, text_colour=None, outline_colour=None, dx=None, dy=None):
        self.text, self.width, self.height = self.create_text(self.raw_text, self.path)

        if new_text is not None:
            self.text, self.width, self.height = self.create_text(new_text, self.path)
        if font_size is not None:
            self.font = pygame.font.Font(self.font_file, font_size)
            if new_text is not None:
                self.text, self.width, self.height = self.create_text(new_text, self.path)
            else:
                self.text, self.width, self.height = self.create_text(self.raw_text, self.path)

        if fill_colour is not None:
            self.fill_colour = list(fill_colour)

        if text_colour is not None:
            self.text_colour = list(text_colour)

        if outline_colour is not None:
            self.outline_colour = list(outline_colour)

        if x is not None:
            self.position.x = x
        if y is not None:
            self.position.y = y
        if dx is not None:
            self.offset.x = dx
        if dy is not None:
            self.offset.y = dy
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if colour is not None:
            self.fill_colour = colour
        if self.centered_x:
            self.centering.x = self.width / 2
        if self.centered_y:
            self.centering.y = self.height / 2
        self.rect.update(delta, self.position.x + self.offset.x, self.position.y + self.offset.y, self.width,
                         self.height, self.fill_colour)

    def draw(self, surface):

        self.rect.draw(surface)

        prev_height = 0
        for line in self.text:
            text_surface, width, height = line
            center = pygame.Vector2(0, 0)
            if self.centered_x:
                center.x = self.width / 2 - width / 2
            # if self.centered_y:
            #     center.y = height / 2
            surface.blit(text_surface,
                         self.position + center - self.centering + pygame.Vector2(0, prev_height) + self.offset)
            prev_height += height


class ButtonLite(LabelLite):

    def __init__(self, pos, text, font_size, func, text_colour=(0, 0, 0), antialias=True, centered_x=True,
                 centered_y=True,
                 filled=False, fill_colour=(150, 150, 150), outlined=False, outline_colour=(0, 0, 0), outline_radius=2,
                 font_file="MontserratBlack-ZVK6J.otf"):
        super().__init__(pos, text, font_size, text_colour, antialias, centered_x, centered_y,
                         filled, fill_colour, outlined, outline_colour, outline_radius,
                         font_file)
        self.func = func

    def is_touching_mouse_pointer(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
                self.position.x - self.centering.x - self.horizontal_padding <= mouse_x <= self.position.x + self.width - self.centering.x + self.horizontal_padding
                and self.position.y - self.centering.y - self.vertical_padding <= mouse_y <= self.position.y + self.height - self.centering.y + self.vertical_padding):
            return True
        return False

    def lighten(self):
        self.fill_colour = (100, 100, 100)

    def darken(self):
        self.fill_colour = (150, 150, 150)

    def update(self, delta, new_text=None, x=None, y=None, width=None, height=None, colour=None, font_size=None):
        super().update(delta, new_text, x, y, width, height, colour, font_size)

        if self.is_touching_mouse_pointer():
            self.lighten()
            if pygame.mouse.get_pressed(3)[0]:
                self.run_function()
        else:
            self.darken()

    def run_function(self):
        return self.func()


class Button(Label):

    def __init__(self, pos, text, font_size, func, text_colour=(0, 0, 0), antialias=True, centered_x=True,
                 centered_y=True, filled=False, fill_colour=(150, 150, 150), outlined=False, outline_colour=(0, 0, 0),
                 outline_radius=2,
                 font_file="MontserratBlack-ZVK6J.otf", path=None, cooldown=100, add_to_list=None):
        super().__init__(pos, text, font_size, text_colour, antialias, centered_x, centered_y,
                         filled, fill_colour, outlined, outline_colour, outline_radius,
                         font_file, path, add_to_list)
        self.fill_colour = list(self.fill_colour)
        self.true_fill_colour = self.fill_colour[:]
        self.func = func
        self.cooldown_amount = cooldown
        self.cooldown = self.cooldown_amount
        self.mouse_was_pressed = False

    def is_touching_mouse_pointer(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
                self.position.x - self.centering.x - self.horizontal_padding <= mouse_x <= self.position.x + self.width - self.centering.x + self.horizontal_padding
                and self.position.y - self.centering.y - self.vertical_padding <= mouse_y <= self.position.y + self.height - self.centering.y + self.vertical_padding):
            return True
        return False

    def lighten(self):
        for i in range(len(self.fill_colour)):
            self.fill_colour[i] = min(self.true_fill_colour[i] + 50, 255)

    def darken(self):
        for i in range(len(self.fill_colour)):
            self.fill_colour[i] = max(self.true_fill_colour[i] - 50, 0)

    def update(self, delta, new_text=None, x=None, y=None, width=None, height=None, colour=None, font_size=None,
               fill_colour=None, text_colour=None, outline_colour=None, dx=None, dy=None):
        super().update(delta, new_text, x, y, width, height, colour, font_size, fill_colour, text_colour,
                       outline_colour, dx=dx, dy=dy)

        if fill_colour is not None:
            self.true_fill_colour = self.fill_colour[:]

        if self.is_touching_mouse_pointer():
            if pygame.mouse.get_pressed(3)[0]:
                self.darken()
                self.mouse_was_pressed = True
            elif self.cooldown == 0 and self.mouse_was_pressed:
                self.run_function()
                self.cooldown = self.cooldown_amount
                self.mouse_was_pressed = False
            else:
                self.mouse_was_pressed = False
        else:
            self.lighten()

        self.cooldown -= delta
        self.cooldown = max(self.cooldown, 0)

    def run_function(self):
        return self.func()


class Slider(Label):

    def __init__(self, pos, text, font_size, var, var_range, text_colour=(0, 0, 0), antialias=True, centered_x=True,
                 centered_y=True, filled=False, fill_colour=(150, 150, 150), outlined=False, outline_colour=(0, 0, 0),
                 outline_radius=2,
                 font_file="MontserratBlack-ZVK6J.otf", path=None, add_to_list=None):
        super().__init__(pos, text, font_size, text_colour, antialias, centered_x, centered_y,
                         filled, fill_colour, outlined, outline_colour, outline_radius,
                         font_file, path, add_to_list)
        self.fill_colour = list(self.fill_colour)
        self.true_fill_colour = self.fill_colour[:]
        self.var = var
        self.range_min, self.range_max = var_range
        self.mouse_was_pressed = False
        self.moved = False
        self.pos = (0,0)

    def is_touching_mouse_pointer(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
                self.position.x - self.centering.x - self.horizontal_padding <= mouse_x <= self.position.x + self.width - self.centering.x + self.horizontal_padding
                and self.position.y - self.centering.y - self.vertical_padding <= mouse_y <= self.position.y + self.height - self.centering.y + self.vertical_padding):
            return True
        return False

    def lighten(self):
        for i in range(len(self.fill_colour)):
            self.fill_colour[i] = min(self.true_fill_colour[i] +50, 255)

    def darken(self):
        for i in range(len(self.fill_colour)):
            self.fill_colour[i] = max(self.true_fill_colour[i] - 0, 0)

    def update(self, delta, new_text=None, x=None, y=None, width=None, height=None, colour=None, font_size=None,
               fill_colour=None, text_colour=None, outline_colour=None, dx=None, dy=None):
        super().update(delta, new_text, x, y, width, height, colour, font_size, fill_colour, text_colour,
                       outline_colour, dx=dx, dy=dy)
        self.rect.update(0,height=self.height + self.vertical_padding * 2)

        if not self.moved:
            move = 0
            if isinstance(self.var, list):
                if len(self.var) == 1:
                    value = self.var[0].split('=')[0]
                    move = self.path[value]
                else:
                    val, path = self.var
                    value = val.split('=')[0]
                    if "self." in value:
                        ind = value.index("self.")
                        value = value[ind + 5:]
                    move = eval("path.%s" % value)

            self.pos = (move * 10 + self.position.x, self.position.y + self.height + self.vertical_padding * 3 / 4)
            self.moved = True

        if fill_colour is not None:
            self.true_fill_colour = self.fill_colour[:]

        if self.is_touching_mouse_pointer():
            if pygame.mouse.get_pressed(3)[0]:
                self.darken()
                return self.slide()
        else:
            self.lighten()
        if isinstance(self.var, list):
            if len(self.var) == 1:
                value = self.var[0].split('=')[0]
                return self.path[value]
            else:
                val, path = self.var
                value = val.split('=')[0]
                if "self." in value:
                    ind = value.index("self.")
                    value = value[ind + 5:]
                return eval("path.%s" % value)

    def slide(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.pos = pygame.Vector2(mouse_x, self.position.y + self.height + self.vertical_padding * 3 /4)
        return round(max(min((mouse_x - self.position.x) / 10, self.range_max),self.range_min)) # Lazy for now

    def draw(self, surface):
        super(Slider, self).draw(surface)
        pygame.draw.line(surface, (150,150,150),(self.position.x, self.position.y + self.height/2 + self.vertical_padding * 2.5),(self.position.x + self.width, self.position.y + self.height/2+ self.vertical_padding * 2.5), 3)
        pygame.draw.circle(surface, (40,40,40), self.pos, 5)

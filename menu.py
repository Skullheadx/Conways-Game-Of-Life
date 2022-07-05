from label import Label, Button
from rectangle import RectangleLite
from setup import *

layouts = [
    [[SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4], [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
     [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]],  # Main Menu Type
    [[SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3], [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4],
     [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], [0, 0], [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]]  # Pop Up layout
]

themes = [
    [[60, (0, 0, 0), True, True, True, False, (255, 255, 255), False, (0, 0, 0), 1],
     [25, (200, 100, 100), True, True, True, False, (255, 255, 255), False, (0, 0, 0), 1],
     [40, (0, 0, 0), True, True, True, True, (250, 250, 250), True, (0, 0, 0), 10]],
    [[60, (0, 0, 0), True, True, True, False, (255, 255, 255), False, (0, 0, 0), 1],
     [25, (200, 100, 100), True, True, True, False, (255, 255, 255), False, (0, 0, 0), 1],
     [20, (0, 0, 0), True, True, True, False, (250, 250, 250), False, (0, 0, 0), 10],
     [30, (0, 0, 0), True, True, True, True, (250, 250, 250), True, (0, 0, 0), 10],
     [40, (0, 0, 0), True, True, True, True, (250, 250, 250), True, (0, 0, 0), 10]]
]


class Menu:

    def __init__(self, title, subtitle, buttons, layout=0, theme=0, path=None, bg_colour=(255, 255, 255)):
        self.background_colour = bg_colour
        if path is None:
            self.path = globals()
        else:
            self.path = path
        self.GUI = []
        self.layout = layouts[layout]
        self.theme = themes[theme]
        # Title
        font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour, outlined, outline_colour, outline_radius = \
            self.theme[0]
        self.GUI.append(
            Label(self.layout[0], [[title]], font_size, text_colour, antialias, centered_x, centered_y, filled,
                  fill_colour,
                  outlined, outline_colour, outline_radius, path=self.path))
        # Subtitle
        font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour, outlined, outline_colour, outline_radius = \
            self.theme[1]
        pos = self.GUI[-1].position + pygame.Vector2(0, self.GUI[-1].height / 2)
        self.GUI.append(
            Label(pos, [[subtitle]], font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour,
                  outlined, outline_colour, outline_radius, path=self.path))
        self.GUI[-1].update(0, y=self.GUI[-1].position.y + self.GUI[-1].height / 2)
        # GUI Buttons/Labels
        self.GUI.append(Container(self.layout[2], buttons, self.theme[2], self.path, 250))

    def update(self, delta):
        for ele in self.GUI:
            ele.update(delta)

    def draw(self, surf):
        surf.fill(self.background_colour)
        for ele in self.GUI:
            ele.draw(surf)
        # pygame.draw.line(surf, (0,0,0), (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))


class Container:

    def __init__(self, pos, elements, theme, path=None, width=0, multi_themes=False):
        if path is None:
            self.path = globals()
        else:
            self.path = path
        self.position = pygame.Vector2(pos)
        self.elements = []
        prev_height = 0
        self.height = 0
        self.width = width
        if multi_themes:
            for i, ele in enumerate(elements):
                font_size, text_colour, antialias, _centered_x, _centered_y, filled, fill_colour, outlined, outline_colour, outline_radius = \
                    theme[i]
                if len(ele) == 2:  # buttons will have function
                    self.elements.append(
                        Button(self.position + pygame.Vector2(0, prev_height), [ele[0]], font_size, ele[1], text_colour,
                               antialias, _centered_x, _centered_y,
                               filled, fill_colour, outlined, outline_colour, outline_radius, path=self.path))
                else:
                    self.elements.append(
                        Label(self.position + pygame.Vector2(0, prev_height), [ele[0]], font_size, text_colour,
                              antialias,
                              _centered_x, _centered_y, filled,
                              fill_colour, outlined, outline_colour, outline_radius, path=self.path))
                prev_height += self.elements[-1].height + (Label.vertical_padding + Label.outline_thickness * 2)
                self.height += prev_height
                self.width = max(self.width, self.elements[-1].width)
        else:
            for i, ele in enumerate(elements):
                font_size, text_colour, antialias, _centered_x, _centered_y, filled, fill_colour, outlined, outline_colour, outline_radius = \
                    theme
                if len(ele) == 2:  # buttons will have function
                    self.elements.append(
                        Button(self.position + pygame.Vector2(0, prev_height), [ele[0]], font_size, ele[1], text_colour,
                               antialias, _centered_x, _centered_y,
                               filled, fill_colour, outlined, outline_colour, outline_radius, path=self.path))
                else:
                    self.elements.append(
                        Label(self.position + pygame.Vector2(0, prev_height), [ele[0]], font_size, text_colour,
                              antialias,
                              _centered_x, _centered_y, filled,
                              fill_colour, outlined, outline_colour, outline_radius, path=self.path))
                prev_height += self.elements[-1].height + (Label.vertical_padding + Label.outline_thickness * 2)
                self.height += prev_height
                self.width = max(self.width, self.elements[-1].width)
        # self.height -= self.elements[0].height/2
        # self.height/=2
        for ele in self.elements:
            ele.update(0, width=self.width)

    def update(self, delta):
        for ele in self.elements:
            ele.update(delta)

    def draw(self, surf):
        for ele in self.elements:
            ele.draw(surf)


class PopUp:

    def __init__(self, pos, title, heading, text, old_scene, theme=1, layout=1, path=None):
        # self.position=pygame.Vector2(pos)
        if path is None:
            self.path = globals()
        else:
            self.path = path
        self.ui = []
        self.layout = layouts[layout]
        self.theme = themes[theme]
        # Title
        font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour, outlined, outline_colour, outline_radius = \
            self.theme[0]
        self.ui.append(
            Label(self.layout[0], [[title]], font_size, text_colour, antialias, centered_x, centered_y, filled,
                  fill_colour,
                  outlined, outline_colour, outline_radius, path=self.path))
        # Subtitle
        font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour, outlined, outline_colour, outline_radius = \
            self.theme[1]
        pos = self.ui[-1].position + pygame.Vector2(0, self.ui[-1].height / 2)
        self.ui.append(
            Label(pos, [[heading]], font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour,
                  outlined, outline_colour, outline_radius, path=self.path))
        self.ui[-1].update(0, y=self.ui[-1].position.y + self.ui[-1].height / 2)
        # Text
        font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour, outlined, outline_colour, outline_radius = \
            self.theme[2]
        pos = self.ui[-1].position + pygame.Vector2(0, self.ui[-1].height / 2)
        self.ui.append(
            Label(pos, [[text]], font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour,
                  outlined, outline_colour, outline_radius, path=self.path))
        self.ui[-1].update(0, y=self.ui[-1].position.y + self.ui[-1].height / 2)

        # Back Button
        def go_back():
            self.path["scene"] = old_scene

        font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour, outlined, outline_colour, outline_radius = \
            self.theme[-2]

        self.ui.append(
            Button(self.layout[-2], [["Back"]], font_size, go_back, text_colour, antialias, False, False, filled,
                   fill_colour, outlined, outline_colour, outline_radius, path=self.path))

        self.width = SCREEN_WIDTH * 2 / 3
        self.height = 0
        for i in self.ui:
            self.height += i.height
            self.width = max(self.width, i.width)
        self.height = max(self.height, SCREEN_HEIGHT * 3 / 4)
        # Rectangle Background
        font_size, text_colour, antialias, centered_x, centered_y, filled, fill_colour, outlined, outline_colour, outline_radius = \
            self.theme[-1]
        self.rect = RectangleLite(
            pygame.Vector2(pos) - pygame.Vector2(self.width + (Label.horizontal_padding + Label.outline_thickness * 2),
                                                 self.height + (
                                                             Label.vertical_padding + Label.outline_thickness * 2)) / 2,
            self.width + (Label.horizontal_padding + Label.outline_thickness * 2) / 2, self.height, centered_x,
            centered_y, filled, fill_colour, outlined, outline_colour, 3, outline_radius)
        # self.UI = Container(self.position, [[title], [heading], [text]], themes[theme], self.path, multi_themes=True)
        # self.rect = RectangleLite(
        #     self.position- pygame.Vector2(self.UI.width + Label.horizontal_padding * 2, self.UI.height + Label.vertical_padding * 2 ) / 2,
        #     self.UI.width + Label.horizontal_padding * 2, self.UI.height + Label.vertical_padding * 2)
        # self.rect = pygame.Rect(pos-pygame.Vector2(self.UI.width, self.UI.height)/2, (self.UI.width, self.UI.height))

    def update(self, delta):
        for ele in self.ui:
            ele.update(delta)

    def draw(self, surf):
        self.rect.draw(surf)
        for ele in self.ui:
            ele.draw(surf)


class PopUp2:

    def __init__(self, pos, title, subtitle, text, viewport):
        self.viewport = viewport
        self.position = pygame.Vector2(pos)
        self.ui = []
        self.title = Label(self.position, [[title]],50,Colour.DARK_GRAY,add_to_list=self.ui)
        self.subtitle = Label(self.title.position + pygame.Vector2(0,self.title.height/2 + Label.vertical_padding + Label.outline_thickness), [[subtitle]],25,Colour.RED,add_to_list=self.ui)
        self.text = Label(self.subtitle.position + pygame.Vector2(0,self.subtitle.height/2 + Label.vertical_padding + Label.outline_thickness), text,20,Colour.DARK_GRAY,add_to_list=self.ui, centered_y=False)
        self.close = False
        self.exit = Button(self.text.position + pygame.Vector2(0,self.text.height + Label.vertical_padding * 6 + Label.outline_thickness),[["   Ok   "]],30,self.exit,Colour.DARK_DARK_GRAY,centered_x=True,centered_y=True, add_to_list=self.ui,
                           filled=True,fill_colour=Colour.GRAY,outlined=True,outline_colour=Colour.DARK_GRAY,outline_radius=3)

        min_x, max_x, min_y, max_y = None, None, None, None
        for ele in self.ui:
            if min_x is None or ele.position.x - ele.width/2 - Label.horizontal_padding - Label.outline_thickness < min_x:
                min_x = ele.position.x - ele.width/2 - Label.horizontal_padding - Label.outline_thickness
            if max_x is None or ele.position.x + ele.width/2 + Label.horizontal_padding + Label.outline_thickness > max_x:
                max_x = ele.position.x + ele.width/2 + Label.horizontal_padding + Label.outline_thickness
            if min_y is None or ele.position.y - ele.height/2 - Label.vertical_padding - Label.outline_thickness < min_y:
                min_y = ele.position.y - ele.height/2 - Label.vertical_padding - Label.outline_thickness
            if max_y is None or ele.position.y + ele.height/2 + Label.vertical_padding + Label.outline_thickness > max_y:
                max_y = ele.position.y + ele.height/2 + Label.vertical_padding + Label.outline_thickness
        self.width = max_x-min_x
        self.height = max_y-min_y + Label.vertical_padding
        self.rect_pos = (min_x, min_y)
        self.rect = RectangleLite(self.rect_pos, self.width, self.height,centered_x=False, centered_y=False,fill_colour=Colour.LIGHT_GRAY)

        self.update(0)

    def exit(self):
        self.close = True

    def update(self, delta):
        if self.close:
            return True
        if pygame.event.peek(pygame.MOUSEBUTTONDOWN, pump=True):
            if not self.rect.get_collision_rect().collidepoint(pygame.mouse.get_pos()):
                return True
        for ele in self.ui:
            ele.update(delta, dy=- self.height/2)
        self.rect.update(delta,y=self.rect_pos[1] - self.height/2)
        return False

    def draw(self, surf):
        self.rect.draw(surf)
        for ele in self.ui:
            ele.draw(surf)

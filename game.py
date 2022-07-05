# I made my own Matrix calculations thing. Did not end well.
# from matrix import Matrix, MultiplyMatrices, print_matrix
import os

from setup import *


class LiveCell:
    side_length = 1
    colour = Colour.BLACK

    def __init__(self, sim_pos, total_offset, taken, live_cells, world, zoom):
        self.simulation_position = pygame.Vector2(sim_pos)
        if tuple(self.simulation_position) not in taken:
            taken.add(tuple(self.simulation_position))
            live_cells.add(self)
        else:
            del self
            return
        self.total_offset = pygame.Vector2(total_offset)
        self.world = world
        self.zoom = zoom
        self.topleft = np.array([[self.simulation_position.x],
                                 [self.simulation_position.y],
                                 [1]])
        # self.bottomright = np.array([[self.simulation_position.x + self.side_length],
        #                         [self.simulation_position.y + self.side_length],
        #                         [1]])

    def get_rect(self):
        translation_matrix = np.array([[1, 0, self.total_offset.x],
                                       [0, 1, self.total_offset.y],
                                       [0, 0, 1]])

        x, y = (self.world @ translation_matrix @ self.topleft)[0:2, 0]

        # br = self.world @ translation_matrix @ self.bottomright
        # x2 = br[0][0]

        side = self.side_length * self.zoom
        # side = x2 - x
        # print(x,y)
        return pygame.Rect(math.ceil(x), math.ceil(y), side, side)
        # return pygame.Rect(x, y, side, side)
        # return pygame.Rect(x1 - side / 2 - self.side_length / 2, y1 - side / 2 - self.side_length / 2, side, side)
        # return pygame.Rect(x1 - side/2, y1 - side/2, side, side)

    def update(self, zoom, relative_movement, transformation_matrix):
        self.zoom = zoom
        self.total_offset += relative_movement
        self.world = transformation_matrix

    @staticmethod
    def is_visible(coords, side, viewport):
        x, y = coords
        if (-side / 2 <= x <= viewport.x + side / 2 and
                -side / 2 <= y <= viewport.y + side / 2):
            return True
        return False

    def draw(self, surf):
        display = self.get_rect()
        viewport = pygame.Vector2(surf.get_size())
        if self.is_visible(display.center, display.width, viewport):
            pygame.draw.rect(surf, self.colour, display)

        # For debugging. pygame.draw.rect(surf,(255,0,0),pygame.Rect(self.simulation_position, (self.side_length,
        # self.side_length))) pygame.draw.rect(surf,Colour.GRAY,pygame.Rect(self.simulation_position,
        # (self.side_length, self.side_length)), 1)


class Brush:

    def __init__(self, brush_size, scatter):
        self.brush_size = brush_size
        self.scatter = scatter

    def set_brush_size(self, brush_size):
        self.brush_size = brush_size

    def increase_brush_size(self, amount=1):
        self.brush_size += amount

    def decrease_brush_size(self, amount=1):
        self.brush_size -= amount

    def toggle_scatter(self):
        self.scatter = not self.scatter

    def paint(self, mouse, total_offset, taken, live_cells, world, affected, is_painting, zoom):
        inv_world = np.linalg.inv(world)
        translation = np.array([[1, 0, -total_offset.x],
                                [0, 1, -total_offset.y],
                                [0, 0, 1]])
        _mouse = np.array([[mouse.x],
                           [mouse.y],
                           [1]])
        sim_pos = (translation @ inv_world @ _mouse)[0:2, 0]
        _is_painting = is_painting
        if _is_painting is None:
            t_x, t_y = sim_pos
            t_x = math.floor(t_x / LiveCell.side_length) * LiveCell.side_length
            t_y = math.floor(t_y / LiveCell.side_length) * LiveCell.side_length
            if (t_x, t_y) in taken:
                _is_painting = False
            else:
                _is_painting = True
        for i in range(-self.brush_size, self.brush_size):
            for j in range(-self.brush_size, self.brush_size):
                if pow(i, 2) + pow(j, 2) < pow(self.brush_size, 2):
                    x, y = sim_pos
                    x = math.floor(x / LiveCell.side_length) * LiveCell.side_length
                    y = math.floor(y / LiveCell.side_length) * LiveCell.side_length

                    x += LiveCell.side_length * i
                    y += LiveCell.side_length * j
                    if (x, y) not in affected:
                        if (x, y) in taken:
                            if _is_painting is None or not _is_painting:
                                if self.scatter:
                                    if random.random() < 0.5:
                                        for cell in live_cells:
                                            if tuple(cell.simulation_position) == (x, y):
                                                live_cells.remove(cell)
                                                taken.remove((x, y))
                                                break
                                else:
                                    for cell in live_cells:
                                        if tuple(cell.simulation_position) == (x, y):
                                            live_cells.remove(cell)
                                            taken.remove((x, y))
                                            break
                        else:
                            if _is_painting is None or _is_painting:
                                if self.scatter:
                                    if random.random() < 0.5:
                                        LiveCell((x, y), total_offset, taken, live_cells, world, zoom)
                                else:
                                    LiveCell((x, y), total_offset, taken, live_cells, world, zoom)
                        affected.add((x, y))
        return _is_painting


class Grid:
    colour = Colour.GRAY

    def __init__(self, zoom, world):
        self.position = pygame.Vector2(0, 0)
        self.zoom = zoom
        self.cell_width = LiveCell.side_length
        # self.lines = []
        # for i in range(SCREEN_WIDTH // (self.cell_width * self.zoom) + 1):
        #     self.lines.append((pygame.Vector2(i * self.cell_width * self.zoom, 0),
        #                        pygame.Vector2(i * self.cell_width * self.zoom, SCREEN_HEIGHT)))
        # for i in range(SCREEN_HEIGHT // (self.cell_width * self.zoom) + 1):
        #     self.lines.append((pygame.Vector2(0,i * self.cell_width * self.zoom),
        #                        pygame.Vector2(SCREEN_WIDTH,i * self.cell_width * self.zoom)))
        self.total_offset = pygame.Vector2(0, 0)
        self.world = world

    def update(self, zoom, relative_movement, world_transformation_matrix):
        self.zoom = zoom
        self.total_offset += relative_movement
        self.world = world_transformation_matrix

    def apply_transformations(self, pt):
        point = np.array([[pt.x],
                          [pt.y],
                          [1]])
        translation_matrix = np.array([[1, 0, self.total_offset.x],
                                       [0, 1, self.total_offset.y],
                                       [0, 0, 1]])
        # return pygame.Vector2(tuple((self.world @ point)[0:2, 0]))
        return pygame.Vector2(tuple((self.world @ translation_matrix @ point)[0:2, 0]))

    def reverse_transformations(self, pt):
        point = np.array([[pt.x],
                          [pt.y],
                          [1]])
        translation_matrix = np.array([[1, 0, -self.total_offset.x],
                                       [0, 1, -self.total_offset.y],
                                       [0, 0, 1]])
        inv_world = np.linalg.inv(self.world)
        return pygame.Vector2(tuple((translation_matrix @ inv_world @ point)[0:2, 0]))

    @staticmethod
    def is_line_visible(start, end, viewport_dimensions, width):  # we only deal with horizontal or vertical lines
        x1, y1 = start
        x2, y2 = end
        if ((-width / 2 <= x1 <= viewport_dimensions.x + width / 2 or
             -width / 2 <= y1 <= viewport_dimensions.y + width / 2) or
                (-width / 2 <= x2 <= viewport_dimensions.x + width / 2 or
                 -width / 2 <= y2 <= viewport_dimensions.y + width / 2)):
            return True
        return False

    def draw(self, surf):
        if self.zoom < 2.5:
            return
        global_position = (self.reverse_transformations(pygame.Vector2(0, 0))) // self.cell_width * self.cell_width
        width = math.ceil(self.zoom / 15)

        viewport_dimensions = pygame.Vector2(surf.get_size())
        # viewport_dimensions = self.reverse_transformations(pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT))
        # print(viewport_dimensions, global_position)

        for i in range(round(viewport_dimensions.x) // math.ceil(self.cell_width) + 1):
            start = self.apply_transformations(global_position + pygame.Vector2(i * self.cell_width, 0))
            end = self.apply_transformations(
                global_position + pygame.Vector2(i * self.cell_width, viewport_dimensions.y))
            if self.is_line_visible(start, end, viewport_dimensions, width):
                pygame.draw.line(surf, self.colour, start, end, width)
        for i in range(round(viewport_dimensions.y) // math.ceil(self.cell_width) + 1):
            start = self.apply_transformations(global_position + pygame.Vector2(0, i * self.cell_width))
            end = self.apply_transformations(
                global_position + pygame.Vector2(viewport_dimensions.x, i * self.cell_width))
            if self.is_line_visible(start, end, viewport_dimensions, width):
                pygame.draw.line(surf, self.colour, start, end, width)
        # for line in self.lines:
        #     start = line[0] + self.total_offset
        #     end = line[1] + self.total_offset
        #
        #     # centering = pygame.Vector2(self.cell_width * self.zoom)/2
        #
        #     pygame.draw.line(surf, Colour.GRAY, self.apply_transformations(start),
        #     self.apply_transformations(end), math.ceil(self.zoom/2))


def get_surrounding():
    out = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            out.append(pygame.Vector2(i, j))
    return out


class Game:
    background_colour = Colour.WHITE
    menu_bg = Colour.LIGHT_GRAY
    menu_text = Colour.DARK_GRAY
    menu_outline = Colour.DARK_GRAY
    display_info_colour = Colour.DARK_GRAY

    starting_zoom = 11

    def __init__(self):
        self.viewport = pygame.Vector2(screen.get_size())

        self.taken = set()
        self.live_cells = set()
        self.zoom = self.starting_zoom
        self.current_zoom = self.starting_zoom
        self.total_offset = pygame.Vector2(0, 0)
        self.world = np.identity(3)
        self.world = self.calculate_world_matrix(self.current_zoom)
        self.inv_world = np.linalg.inv(self.world)

        self.is_simulating = False
        self.surrounding = get_surrounding()

        self.labels = []

        self.mode = "Dark"
        self.toggle_mode()
        self.mode_button = Button((100, self.viewport.y), [[[f"{self.mode=}", self]]], 15, self.toggle_mode,
                                  centered_x=False,
                                  centered_y=False, path=globals(), cooldown=250,
                                  filled=True, outlined=True, outline_radius=7,
                                  fill_colour=self.menu_bg, text_colour=self.menu_text,
                                  outline_colour=self.menu_outline, add_to_list=self.labels)

        self.state = "Run"
        self.start_button = Button((0, 0), [[[f"{self.state=}", self]]], 20, self.run, centered_x=False,
                                   centered_y=False, path=globals(), cooldown=200,
                                   filled=True, outlined=True, outline_radius=4,
                                   fill_colour=self.menu_bg, text_colour=self.menu_text,
                                   outline_colour=self.menu_outline, add_to_list=self.labels)

        self.step_button = Button((0, 0), [["Step"]], 15, self.tick, centered_x=False,
                                  centered_y=False, path=globals(), cooldown=200,
                                  filled=True, outlined=True, outline_radius=4,
                                  fill_colour=self.menu_bg, text_colour=self.menu_text,
                                  outline_colour=self.menu_outline, add_to_list=self.labels)
        self.clear_button = Button((0, 0), [["Clear"]], 15, self.clear, centered_x=False,
                                   centered_y=False, path=globals(), cooldown=200,
                                   filled=True, outlined=True, outline_radius=4,
                                   fill_colour=self.menu_bg, text_colour=self.menu_text,
                                   outline_colour=self.menu_outline, add_to_list=self.labels)
        self.randomize_button = Button((0, 0), [["Randomize"]], 15, self.randomize, centered_x=False,
                                       centered_y=False, path=globals(), cooldown=200,
                                       filled=True, outlined=True, outline_radius=4,
                                       fill_colour=self.menu_bg, text_colour=self.menu_text,
                                       outline_colour=self.menu_outline, add_to_list=self.labels)
        self.brush_size = 1
        self.brush_size_slider = Slider((0, 0), [["Brush Size: ", [f"{self.brush_size=}", self]]], 15,
                                        [f"{self.brush_size=}", self], (1, 10), centered_x=False,
                                        centered_y=False, path=globals(),
                                        filled=True, outlined=True, outline_radius=4,
                                        fill_colour=self.menu_bg, text_colour=self.menu_text,
                                        outline_colour=self.menu_outline, add_to_list=self.labels)
        self.is_scattering = False
        self.brush_scatter_button = Button((0, 0), [["Scatter: ", [f"{self.is_scattering=}", self]]], 15,
                                           self.toggle_scatter, centered_x=False,
                                           centered_y=False, path=globals(), cooldown=200,
                                           filled=True, outlined=True, outline_radius=4,
                                           fill_colour=self.menu_bg, text_colour=self.menu_text,
                                           outline_colour=self.menu_outline, add_to_list=self.labels)
        self.import_button = Button((0, 0), [["Import"]], 15, self.import_pattern, centered_x=False,
                                    centered_y=False, path=globals(), cooldown=200,
                                    filled=True, outlined=True, outline_radius=4,
                                    fill_colour=self.menu_bg, text_colour=self.menu_text,
                                    outline_colour=self.menu_outline, add_to_list=self.labels)
        self.export_button = Button((0, 0), [["Export"]], 15, self.export_pattern, centered_x=False,
                                    centered_y=False, path=globals(), cooldown=200,
                                    filled=True, outlined=True, outline_radius=4,
                                    fill_colour=self.menu_bg, text_colour=self.menu_text,
                                    outline_colour=self.menu_outline, add_to_list=self.labels)
        self.about = None
        self.about_button = Button((0, 0), [["About"]], 15, self.to_about, centered_x=False,
                                   centered_y=False, path=globals(), cooldown=200,
                                   filled=True, outlined=True, outline_radius=4,
                                   fill_colour=self.menu_bg, text_colour=self.menu_text,
                                   outline_colour=self.menu_outline, add_to_list=self.labels)

        self.show_grid = True
        self.grid_button = Button((0, self.viewport.y), [["Toggle Grid"]], 15, self.toggle_grid, centered_x=False,
                                  centered_y=False, path=globals(), cooldown=250,
                                  filled=True, outlined=True, outline_radius=7,
                                  fill_colour=self.menu_bg, text_colour=self.menu_text,
                                  outline_colour=self.menu_outline, add_to_list=self.labels)

        self.zoom_in_button = Button((0, 50), [[" + "]], 15, self.zoom_in, centered_x=False,
                                     centered_y=False, path=globals(), cooldown=100,
                                     filled=True, outlined=True, outline_radius=5,
                                     fill_colour=self.menu_bg, text_colour=self.menu_text,
                                     outline_colour=self.menu_outline, add_to_list=self.labels)
        self.zoom_out_button = Button((0, 50), [[" – "]], 15, self.zoom_out, centered_x=True,
                                      centered_y=False, path=globals(), cooldown=100,
                                      filled=True, outlined=True, outline_radius=5,
                                      fill_colour=self.menu_bg, text_colour=self.menu_text,
                                      outline_colour=self.menu_outline, add_to_list=self.labels)

        self.home_button = Button((0, 100), [["Home"]], 15, self.go_home, centered_x=False,
                                  centered_y=False, path=globals(), cooldown=250,
                                  filled=True, outlined=True, outline_radius=5,
                                  fill_colour=self.menu_bg, text_colour=self.menu_text,
                                  outline_colour=self.menu_outline, add_to_list=self.labels)

        self.upd_delay_MS = 125
        self.upd_event = pygame.USEREVENT
        pygame.time.set_timer(self.upd_event, self.upd_delay_MS)
        self.speed_up_button = Button((0, 150), [[">>"]], 15, self.speed_up, centered_x=False,
                                      centered_y=False, path=globals(), cooldown=100,
                                      filled=True, outlined=True, outline_radius=5,
                                      fill_colour=self.menu_bg, text_colour=self.menu_text,
                                      outline_colour=self.menu_outline, add_to_list=self.labels)
        self.slow_down_button = Button((0, 150), [["<<"]], 15, self.slow_down, centered_x=True,
                                       centered_y=False, path=globals(), cooldown=100,
                                       filled=True, outlined=True, outline_radius=5,
                                       fill_colour=self.menu_bg, text_colour=self.menu_text,
                                       outline_colour=self.menu_outline, add_to_list=self.labels)

        self.population = len(self.live_cells)
        self.generation = 0
        self.fps = fps
        self.mouse = pygame.mouse.get_pos()
        self.zoom_percent = "{:,}".format(round(self.zoom * 100 / self.starting_zoom))
        self.cpu_usage = psutil.cpu_percent()
        self.display_info = Label((self.viewport.x, self.viewport.y),
                                  [["Pop: ", [f"{self.population=}", self],
                                    " | Gen: ", [f"{self.generation=}", self],
                                    " | FPS: ", [f"{self.fps=}", self],
                                    " | ", [f"{self.mouse=}", self],
                                    " | Zoom: ", [f"{self.zoom_percent=}", self], "%",
                                    " | CPU: ", [f"{self.cpu_usage=}", self], "%"
                                    ]],
                                  15, centered_x=False, centered_y=False, path=globals(),
                                  text_colour=self.display_info_colour, add_to_list=self.labels)

        self.brush = Brush(self.brush_size, self.is_scattering)
        self.affected = set()
        self.is_painting = None

        self.grid = Grid(self.zoom, self.world)

        self.show_ui = True

        self.go_home()

    def toggle_ui(self):
        self.show_ui = not self.show_ui

    def to_about(self):
        self.about = PopUp2((self.viewport.x / 2, self.viewport.y / 2), "Conway's Game Of Life", "Failure Studios",
                            [["Conway's Game of Life is a zero player game."],
                             ["Its evolution is determined by its initial state,"],
                             ["LMB and drag to move, RMB to add/delete cells"],
                             ["The rules are:"],
                             ["1. Any live cell with fewer than two live neighbours dies, as if by underpopulation."],
                             ["2. Any live cell with two or three live neighbours lives on to the next generation."],
                             ["3. Any live cell with more than three live neighbours dies, as if by overpopulation."],
                             [
                                 "4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction."]],
                            self.viewport)

    def import_pattern(self):
        # Get RLE Files from https://copy.sh/life/examples/
        root = tk.Tk()
        root.withdraw()

        filename = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                              filetypes=(("RLE files", "*.RLE"), ("all files", "*.*")))
        if filename == '':
            return
        with open(filename, 'r', encoding='utf-8') as f:
            file_contents = f.read().split("\n")

        x, y = 0, 0
        index = 0
        for i, thing in enumerate(file_contents):
            if thing[0] == 'x':
                temp = thing.split(',')
                temp2 = temp[0][::-1]
                x = int(temp2[:temp2.index(" ")][::-1]) // 2
                temp2 = temp[1][::-1]
                y = int(temp2[:temp2.index(" ")][::-1]) // 2
                index = i + 1
                break

        pattern = decode("".join(file_contents[index:]))
        offset_matrix = np.array([[1, 0, -self.total_offset.x], [0, 1, -self.total_offset.y], [0, 0, 1]])
        pos = tuple(map(round, (offset_matrix @ self.inv_world @ np.array([[0], [0], [1]]))[0:2, 0]))

        x += pos[0]
        y += pos[1]
        pos = (x, y)

        for i in pattern:
            if i == 'o':
                LiveCell((x, y), self.total_offset, self.taken, self.live_cells, self.world, self.zoom)
                x += 1
            elif i == 'b':
                x += 1
            elif i == '$':
                x = pos[0]
                y += 1
            elif i == '!':
                break

    def export_pattern(self):
        if len(self.live_cells) == 0:
            return
        min_x, max_x, min_y, max_y = None, None, None, None
        for cell in self.live_cells:
            if min_x is None or cell.simulation_position.x < min_x:
                min_x = cell.simulation_position.x
            elif max_x is None or cell.simulation_position.x > max_x:
                max_x = cell.simulation_position.x
            if min_y is None or cell.simulation_position.y < min_y:
                min_y = cell.simulation_position.y
            elif max_y is None or cell.simulation_position.y > max_y:
                max_y = cell.simulation_position.y

        min_x = round(min_x)
        max_x = round(max_x)
        min_y = round(min_y)
        max_y = round(max_y)

        out = "x = %s, y = %s, rule = b3/s23\n" % (min_x, min_y)
        for j in range(min_y, max_y, LiveCell.side_length):
            for i in range(min_x, max_x, LiveCell.side_length):
                if (i, j) in self.taken:
                    out += "o"
                else:
                    out += 'b'
            out += '$'
        out += '!'

        new_out = ""
        skip = 0
        for ind, val in enumerate(out):
            if skip > 0:
                skip -= 1
                continue
            if ind != len(out) - 1:
                if out[ind + 1] == val:
                    count = 0
                    for ind2, val2 in enumerate(out[ind + 1:]):
                        if val == val2:
                            count += 1
                        else:
                            skip = ind2
                            break
                    new_out += str(count) + val
                else:
                    new_out += val
            else:
                new_out += val
        filename = "GameOfLife"
        temp = 0
        print()
        while True:
            try:
                if temp == 0:
                    with open(os.path.join(os.path.join(os.environ["HOMEPATH"], "Documents"), f"{filename}.RLE"),
                              'x') as f:
                        f.write(new_out)
                else:
                    with open(os.path.join(os.path.join(os.environ["HOMEPATH"], "Documents"), f"{filename}{temp}.RLE"),
                              'x') as f:
                        f.write(new_out)
                break
            except FileExistsError:
                temp += 1

    def run(self):
        self.is_simulating = not self.is_simulating
        if self.is_simulating:
            self.state = "Stop"
        else:
            self.state = "Run"

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def toggle_mode(self):
        if self.mode == "Dark":
            self.mode = "Light"
            # Dark Mode
            LiveCell.colour = Colour.LIGHT_GRAY
            Grid.colour = Colour.DARK_GRAY
            self.background_colour = Colour.BLACK
            self.menu_bg = Colour.DARK_GRAY
            self.menu_text = Colour.DARK_DARK_GRAY
            self.menu_outline = Colour.BLACK
            self.display_info_colour = Colour.GRAY
        else:
            self.mode = "Dark"
            # Light Mode Ewwww!
            LiveCell.colour = Colour.BLACK
            Grid.Colour = Colour.GRAY
            self.background_colour = Colour.WHITE
            self.menu_bg = Colour.LIGHT_GRAY
            self.menu_text = Colour.DARK_GRAY
            self.menu_outline = Colour.DARK_GRAY
            self.display_info_colour = Colour.DARK_GRAY

    def toggle_scatter(self):
        self.is_scattering = not self.is_scattering
        self.brush.scatter = self.is_scattering

    def go_home(self):
        # Not accurate because when u zoom in and out it translate stuff a bit
        center = tuple((self.inv_world @ np.array([[0], [0], [1]]))[0:2, 0])
        self.total_offset = pygame.Vector2(center)
        for cell in self.live_cells:
            cell.total_offset = pygame.Vector2(center)
        self.grid.total_offset = pygame.Vector2(center)

    # def fit(self):
    #     min_x = None
    #     min_y = None
    #     max_x = None
    #     max_y = None
    #
    #     for cell in self.live_cells:
    #         if min_x is None or cell.simulation_position.x < min_x:
    #             min_x = cell.simulation_position.x
    #         elif max_x is None or cell.simulation_position.x > max_x:
    #             max_x = cell.simulation_position.x + cell.side_length
    #         if min_y is None or cell.simulation_position.y < min_y:
    #             min_y = cell.simulation_position.y
    #         elif max_y is None or cell.simulation_position.y > max_y:
    #             max_y = cell.simulation_position.y + cell.side_length
    #     center = pygame.Vector2((max_x - min_x) / 2, (max_y - min_y) / 2)
    #
    #     z = # idk what to do here
    #     self.calculate_world_matrix(z, center)
    #
    #     self.total_offset = pygame.Vector2(0, 0)
    #     for cell in self.live_cells:
    #         cell.total_offset = pygame.Vector2(0, 0)
    #     self.grid.total_offset = pygame.Vector2(0, 0)

    def calculate_world_matrix(self, current_zoom, pos=None):
        if pos is not None:
            mouse_pos = pos
        else:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        translation_matrix = np.array([[1, 0, mouse_pos.x],
                                       [0, 1, mouse_pos.y],
                                       [0, 0, 1]])
        translation_matrix_2 = np.array([[1, 0, -mouse_pos.x],
                                         [0, 1, -mouse_pos.y],
                                         [0, 0, 1]])

        scale_matrix = np.array([[current_zoom, 0, 0],
                                 [0, current_zoom, 0],
                                 [0, 0, 1]])

        return translation_matrix @ scale_matrix @ translation_matrix_2 @ self.world

    def calculate_zoom(self, scroll):
        if scroll < 0:  # and self.zoom * 0.75 >= 3.5:
            self.zoom *= 0.75
            return -0.25
        elif scroll > 0:
            self.zoom *= 1.25
            return 0.25
        # current_zoom = round(current_zoom, 3)

    def zoom_in(self):
        self.current_zoom += self.calculate_zoom(1)
        self.world = self.calculate_world_matrix(self.current_zoom,
                                                 pos=pygame.Vector2(self.viewport.x, self.viewport.y) / 2)
        self.inv_world = np.linalg.inv(self.world)

    def zoom_out(self):
        self.current_zoom += self.calculate_zoom(-1)
        self.world = self.calculate_world_matrix(self.current_zoom,
                                                 pos=pygame.Vector2(self.viewport.x, self.viewport.y) / 2)
        self.inv_world = np.linalg.inv(self.world)

    def speed_up(self):
        pygame.time.set_timer(self.upd_event, 0)
        self.upd_delay_MS -= 10
        self.upd_delay_MS = max(self.upd_delay_MS, 5)
        pygame.time.set_timer(self.upd_event, self.upd_delay_MS)

    def slow_down(self):
        pygame.time.set_timer(self.upd_event, 0)
        self.upd_delay_MS += 10
        pygame.time.set_timer(self.upd_event, self.upd_delay_MS)

    def clear(self):
        self.taken = set()
        self.live_cells = set()

    def randomize(self):
        offset_matrix = np.array([[1, 0, -self.total_offset.x], [0, 1, -self.total_offset.y], [0, 0, 1]])
        x1, y1 = tuple(map(round, tuple((offset_matrix @ self.inv_world @ np.array([[0], [0], [1]]))[0:2, 0])))
        x2, y2 = tuple(map(round, tuple(
            (offset_matrix @ self.inv_world @ np.array([[self.viewport.x], [self.viewport.y], [1]]))[0:2, 0])))
        for x in range(x1, x2, LiveCell.side_length):
            for y in range(y1, y2, LiveCell.side_length):
                if random.random() < 0.25:
                    x = math.floor(x / LiveCell.side_length) * LiveCell.side_length
                    y = math.floor(y / LiveCell.side_length) * LiveCell.side_length
                    LiveCell((x, y), self.total_offset, self.taken, self.live_cells, self.world, self.zoom)

    def update(self, delta):
        self.viewport = pygame.Vector2(screen.get_size())

        if self.about is not None:
            if self.about.update(delta):
                self.about = None
            return

        # Receive inputs and calculate zoom
        self.current_zoom = 1
        for event in pygame.event.get(
                (pygame.MOUSEWHEEL, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, self.upd_event, pygame.KEYUP)):
            if event.type == pygame.MOUSEWHEEL:
                self.current_zoom += self.calculate_zoom(event.y)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                pygame.mouse.get_rel()
            elif event.type == pygame.MOUSEBUTTONUP:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            elif event.type == self.upd_event:
                if self.is_simulating:
                    self.tick()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F1:
                    self.toggle_ui()

        # Calculate world transformation matrix
        self.world = self.calculate_world_matrix(self.current_zoom)
        self.inv_world = np.linalg.inv(self.world)

        # Determine relative mouse position or paint onto screen
        mouse_rel = pygame.Vector2(0, 0)
        mouse = pygame.mouse.get_pressed(3)
        if mouse[0] and not self.brush_size_slider.rect.get_collision_rect().collidepoint(pygame.mouse.get_pos()):
            mouse_rel = pygame.Vector2(pygame.mouse.get_rel()) / self.zoom
            self.total_offset += mouse_rel
        elif mouse[2]:
            self.is_painting = self.brush.paint(pygame.Vector2(pygame.mouse.get_pos()), self.total_offset, self.taken,
                                                self.live_cells, self.world,
                                                self.affected, self.is_painting, self.zoom)
        elif not mouse[2]:
            self.affected = set()
            self.is_painting = None
        # Update buttons
        if self.show_ui:
            self.start_button.update(delta, x=Label.horizontal_padding + Label.outline_thickness,
                                     y=Label.vertical_padding + Label.outline_thickness,
                                     fill_colour=self.menu_bg, text_colour=self.menu_text,
                                     outline_colour=self.menu_outline)

            self.about_button.update(delta,
                                     x=self.viewport.x - Label.horizontal_padding
                                       - Label.outline_thickness - self.about_button.width,
                                     y=Label.vertical_padding + Label.outline_thickness,
                                     fill_colour=self.menu_bg, text_colour=self.menu_text,
                                     outline_colour=self.menu_outline)

            self.export_button.update(delta,
                                      x=self.about_button.position.x - self.export_button.width - Label.horizontal_padding * 2 - Label.outline_thickness,
                                      y=Label.vertical_padding + Label.outline_thickness,
                                      fill_colour=self.menu_bg, text_colour=self.menu_text,
                                      outline_colour=self.menu_outline)
            self.import_button.update(delta,
                                      x=self.export_button.position.x - self.import_button.width - Label.horizontal_padding * 2 - Label.outline_thickness,
                                      y=Label.vertical_padding + Label.outline_thickness,
                                      fill_colour=self.menu_bg, text_colour=self.menu_text,
                                      outline_colour=self.menu_outline)

            self.brush_size = self.brush_size_slider.update(delta,
                                                            x=self.import_button.position.x - self.brush_size_slider.width - Label.horizontal_padding * 2 - Label.outline_thickness,
                                                            y=Label.vertical_padding + Label.outline_thickness,
                                                            fill_colour=self.menu_bg, text_colour=self.menu_text,
                                                            outline_colour=self.menu_outline)
            self.brush.set_brush_size(self.brush_size)
            self.brush_scatter_button.update(delta,
                                             x=self.brush_size_slider.position.x - self.brush_scatter_button.width - Label.horizontal_padding * 2 - Label.outline_thickness,
                                             y=Label.vertical_padding + Label.outline_thickness,
                                             fill_colour=self.menu_bg, text_colour=self.menu_text,
                                             outline_colour=self.menu_outline)
            self.randomize_button.update(delta,
                                         x=self.brush_scatter_button.position.x - self.randomize_button.width - Label.horizontal_padding * 2 - Label.outline_thickness,
                                         y=Label.vertical_padding + Label.outline_thickness,
                                         fill_colour=self.menu_bg, text_colour=self.menu_text,
                                         outline_colour=self.menu_outline)
            self.clear_button.update(delta,
                                     x=self.randomize_button.position.x - self.clear_button.width - Label.horizontal_padding * 2 - Label.outline_thickness,
                                     y=Label.vertical_padding + Label.outline_thickness,
                                     fill_colour=self.menu_bg, text_colour=self.menu_text,
                                     outline_colour=self.menu_outline)
            self.step_button.update(delta,
                                    x=self.clear_button.position.x - self.step_button.width - Label.horizontal_padding * 2 - Label.outline_thickness,
                                    y=Label.vertical_padding + Label.outline_thickness,
                                    fill_colour=self.menu_bg, text_colour=self.menu_text,
                                    outline_colour=self.menu_outline)

            self.grid_button.update(delta, x=Label.horizontal_padding + Label.outline_thickness,
                                    y=self.viewport.y - Label.vertical_padding - Label.outline_thickness - self.grid_button.height,
                                    fill_colour=self.menu_bg, text_colour=self.menu_text,
                                    outline_colour=self.menu_outline)
            self.mode_button.update(delta,
                                    x=Label.horizontal_padding * 2 + Label.outline_thickness + self.grid_button.width + self.grid_button.position.x,
                                    y=self.viewport.y - Label.vertical_padding - Label.outline_thickness - self.mode_button.height,
                                    fill_colour=self.menu_bg, text_colour=self.menu_text,
                                    outline_colour=self.menu_outline)

            self.zoom_in_button.update(delta, x=Label.horizontal_padding + Label.outline_thickness,
                                       y=Label.vertical_padding * 2 + Label.outline_thickness + self.start_button.position.y + self.start_button.height,
                                       fill_colour=self.menu_bg, text_colour=self.menu_text,
                                       outline_colour=self.menu_outline)
            self.zoom_out_button.update(delta, x=self.zoom_in_button.position.x + self.zoom_in_button.width / 2,
                                        y=Label.vertical_padding + Label.outline_thickness + self.zoom_in_button.position.y + self.zoom_in_button.height,
                                        fill_colour=self.menu_bg, text_colour=self.menu_text,
                                        outline_colour=self.menu_outline)
            self.slow_down_button.update(delta, x=self.zoom_in_button.position.x + self.zoom_in_button.width / 2,
                                         y=Label.vertical_padding * 2 + Label.outline_thickness + self.home_button.position.y + self.home_button.height,
                                         fill_colour=self.menu_bg, text_colour=self.menu_text,
                                         outline_colour=self.menu_outline)
            self.speed_up_button.update(delta,
                                        x=self.slow_down_button.position.x + self.slow_down_button.width / 2 + Label.horizontal_padding + Label.outline_thickness,
                                        y=Label.vertical_padding * 2 + Label.outline_thickness + self.home_button.position.y + self.home_button.height,
                                        fill_colour=self.menu_bg, text_colour=self.menu_text,
                                        outline_colour=self.menu_outline)
            self.home_button.update(delta, x=Label.horizontal_padding + Label.outline_thickness,
                                    y=Label.vertical_padding * 2 + Label.outline_thickness + self.zoom_out_button.position.y + self.zoom_out_button.height,
                                    fill_colour=self.menu_bg, text_colour=self.menu_text,
                                    outline_colour=self.menu_outline)
            self.population = len(self.live_cells)
            self.fps = round(clock.get_fps())
            self.cpu_usage = psutil.cpu_percent()
            self.zoom_percent = "{:,}".format(round(self.zoom * 100 / self.starting_zoom, 2))
            self.mouse = tuple(
                map(round,
                    (self.inv_world @ np.array([[pygame.mouse.get_pos()[0]], [pygame.mouse.get_pos()[1]], [1]]))[0:2, 0]))
            # self.display_info.update(delta, x=self.display_info.position.x - self.display_info.width,
            #                          y=self.display_info.position.y - Label.vertical_padding + Label.outline_thickness)
            self.display_info.update(delta,
                                     x=self.viewport.x - self.display_info.width - Label.horizontal_padding - Label.outline_thickness,
                                     y=self.viewport.y - self.display_info.height - Label.vertical_padding - Label.outline_thickness,
                                     fill_colour=self.menu_bg, text_colour=self.display_info_colour,
                                     outline_colour=self.menu_text)

        self.grid.update(self.zoom, mouse_rel, self.world)

        # Update cells with new info
        for cell in self.live_cells:
            cell.update(self.zoom, mouse_rel, self.world)
        # print(self.upd_delay_MS)

    def tick(self):
        self.generation += 1
        next_tick = set()
        next_taken = set()
        for cell in self.live_cells:
            neighbors = 0
            for n in self.surrounding:
                neighbor = n * LiveCell.side_length + cell.simulation_position
                if tuple(neighbor) in self.taken:
                    neighbors += 1
                else:
                    neighbors_neighbors = 0
                    for n_n in self.surrounding:  # don't account for neighbor pos to get cool pattern
                        neighbor_neighbor = n_n * LiveCell.side_length + neighbor
                        if tuple(neighbor_neighbor) in self.taken:
                            neighbors_neighbors += 1
                    if neighbors_neighbors == 3:
                        LiveCell(neighbor, cell.total_offset, next_taken, next_tick, self.world, self.zoom)
            if neighbors == 2 or neighbors == 3:
                LiveCell(cell.simulation_position, cell.total_offset, next_taken, next_tick, self.world, self.zoom)
        self.live_cells = next_tick.copy()
        self.taken = next_taken.copy()

    def draw(self, surf):
        if self.about is not None:
            self.about.draw(surf)
            return
        surf.fill(self.background_colour)
        for cell in self.live_cells:
            cell.draw(surf)
        if self.show_grid:
            self.grid.draw(surf)
        if self.show_ui:
            for l in self.labels:
                l.draw(surf)

# TODO
# Brush Controls
# Reference:https://copy.sh/life/?pattern=halfmaxv3

#import Room
import movement
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, BooleanProperty, OptionProperty
from kivy.graphics import Triangle, Rectangle, Line, Color
from kivy.clock import Clock


class Room:

    def print_f(room, flag):
        if flag == 'R':
            for row in room:
                for cell in row:
                    print(cell, end=' ')
                print('\n')
        elif flag == 'RR':
            for row in room:
                for cell in row:
                    print(cell, end=' ')
                print('\n')


class Functions:

    def been_in_row(robot_room):
        for rows in range(1, len(robot_room)-1):
            count = 0
            for cell in range(1, len(robot_room[rows]) - 1):
                if robot_room[rows][cell] == 'k' or robot_room[rows][cell] == 'S' or robot_room[rows][cell] == 'E':
                    break
                else:
                    count += 1
            if count == (len(robot_room[rows])-2):
                return False
        return True

    def is_unknown_region(closest_unknown, robot_room):
        closest_unknown.clear()
        left_wall = False
        right_wall = False
        for line in range(len(robot_room) - 2, 0, -1):
            for column in range(1, len(robot_room[line])-1):
                if robot_room[line][column] == 'u':
                    for x in range(column-1, 0, -1):
                        if robot_room[line][x] == 'w':
                            left_wall = True
                            break
                    for x in range(column+1, len(robot_room[0])-1):
                        if robot_room[line][x] == 'w':
                            right_wall = True
                            break
                    if Functions.cant_get_there(robot_room, line, column) or (right_wall and left_wall):
                        robot_room[line][column] = 'w'
                        left_wall = False
                        right_wall = False
                    else:
                        closest_unknown.append(line)
                        closest_unknown.append(column)
                        return True
        return False

    def cant_get_there(robot_room, row, col):
        for i in range(row - 1, -1, -1):
            if robot_room[i][col] == 'k' or robot_room[i][col] == '2k':
                return False
            if robot_room[i][col] == 'w':
                for j in range(col + 1, len(robot_room[i])):
                    if robot_room[i][j] == 'k' or robot_room[i][j] == '2k':
                        return False
                    if robot_room[i][j] == 'w':
                        for k in range(i + 1, row+2):
                            if robot_room[k][j] == 'k' or robot_room[k][j] == '2k':
                                return False
                            if robot_room[k][j] == 'w':
                                for w in range(j - 1, col - 2, -1):
                                    if robot_room[k][w] == 'k' or robot_room[k][w] == '2k':
                                        return False
                                    if robot_room[k][w] == 'w':
                                        for z in range(k - 1, i - 1, -1):
                                            if robot_room[z][w] == 'k' or robot_room[z][w] == '2k':
                                                return False

                                            if robot_room[z][w] != 'w':
                                                break
                                            if z == i:
                                                for rows in range(i + 1, k):
                                                    for cell in range(col, j):
                                                        robot_room[rows][cell] = 'w'
                                                return True
                                    else:
                                        break
                            else:
                                break
                    else:
                        break
        return False

    def sensor_checking(room, robot_room, row, col):
        if room[row + 1][col] == 'w' and row < len(robot_room) - 2:
            robot_room[row + 1][col] = 'w'
        if room[row - 1][col] == 'w' and row > 1:
            robot_room[row - 1][col] = 'w'
        if room[row][col + 1] == 'w' and row < len(robot_room) - 2:
            robot_room[row][col + 1] = 'w'
        if room[row][col - 1] == 'w' and row > 1:
            robot_room[row][col - 1] = 'w'

class ScreenManagement(ScreenManager):
    pass


class MainScreen(Screen):
    pass


class AutoScreen(Screen):

    room = []
    robot_room = []
    closest_unknown = []
    done_gap_filling = False
    done_region_filling = False
    flag = 'r'
    bot = 'b'
    row = 0
    col = 0

    def go(self, **kwargs):
        super(AutoScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.start, 0.1)

    def stop(self):
        Clock.unschedule(self.start)

    def start(self, *args):
        #  Region Filling
        if not self.done_region_filling:
            if Functions.been_in_row(self.robot_room):
                self.done_region_filling = True
            elif self.room[self.row][self.col+1] != 'w' and self.flag == 'r'\
                    and self.robot_room[self.row][self.col+1] != 'k':
                if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                    self.robot_room[self.row+1][self.col] = 'w'
                if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                    self.robot_room[self.row-1][self.col] = 'w'
                self.col = movement.rn(self.row, self.col, self.room, self.bot)
                self.robot_room[self.row][self.col] = 'k'
                self.plot(self.row, self.col)

            elif self.room[self.row][self.col-1] != 'w' and self.flag == 'l'\
                    and self.robot_room[self.row][self.col-1] != 'k':
                if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                    self.robot_room[self.row+1][self.col] = 'w'
                if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                    self.robot_room[self.row-1][self.col] = 'w'
                self.col = movement.ln(self.row, self.col, self.room, self.bot)
                self.robot_room[self.row][self.col] = 'k'
                self.plot(self.row, self.col)

            elif self.room[self.row][self.col+1] == 'w' and self.flag == 'r':
                # Obstacle
                if self.col < (len(self.robot_room[self.row])-2):
                    self.robot_room[self.row][self.col+1] = 'w'
                # 90 Deg to the Right
                if self.room[self.row+1][self.col] != 'w':
                    if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                        self.robot_room[self.row-1][self.col] = 'w'
                    self.row = movement.dn(self.row, self.col, self.room, self.bot)
                    self.robot_room[self.row][self.col] = 'k'
                    self.plot(self.row, self.col)
                    if self.room[self.row][self.col+1] == 'w' and self.col <= len(self.robot_room)-2:
                        self.robot_room[self.row][self.col + 1] = 'w'
                    if self.room[self.row][self.col-1] == 'w':
                        self.robot_room[self.row][self.col-1] = 'w'
                    self.flag = 'l'
                else:  # Dead Lock - Reverse
                    self.flag = 'l'
                    if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room)-2:
                        self.robot_room[self.row+1][self.col] = 'w'
                    if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                        self.robot_room[self.row-1][self.col] = 'w'
                    if not(Functions.been_in_row(self.robot_room)):
                        if self.room[self.row+1][self.col] == 'w':
                            self.robot_room[self.row+1][self.col] = 'w'
                            self.col = movement.ln(self.row, self.col, self.room, self.bot)
                            self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            if self.room[self.row][self.col-1] == 'w':
                                self.robot_room[self.row][self.col - 1] = 'w'
                                self.row = movement.dn(self.row, self.col, self.room, self.bot)
                                self.plot(self.row, self.col)
                        if self.room[self.row][self.col+1] == 'w':
                            self.robot_room[self.row][self.col + 1] = 'w'
                        if self.room[self.row][self.col-1] == 'w':
                            self.robot_room[self.row][self.col - 1] = 'w'
                        self.robot_room[self.row][self.col] = 'k'
                        self.plot(self.row, self.col)

            elif self.room[self.row][self.col-1] == 'w' and self.flag == 'l':
                # Obstacle
                if self.col > 1:
                    self.robot_room[self.row][self.col-1] = 'w'
                # 90 Deg to the Left
                if self.room[self.row+1][self.col] != 'w':
                    if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                        self.robot_room[self.row-1][self.col] = 'w'
                    self.row = movement.dn(self.row, self.col, self.room, self.bot)
                    self.robot_room[self.row][self.col] = 'k'
                    self.plot(self.row, self.col)
                    if self.room[self.row][self.col+1] == 'w':
                        self.robot_room[self.row][self.col + 1] = 'w'
                    if self.room[self.row][self.col-1] == 'w':
                        self.robot_room[self.row][self.col - 1] = 'w'
                    self.flag = 'r'
                else:  # Dead Lock - Reverse
                    self.flag = 'r'
                    if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                        self.robot_room[self.row+1][self.col] = 'w'
                    if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                        self.robot_room[self.row-1][self.col] = 'w'
                    if not (Functions.been_in_row(self.robot_room)):
                        if self.room[self.row+1][self.col] == 'w':
                            self.robot_room[self.row+1][self.col] = 'w'
                            self.col = movement.rn(self, self.row, self.col, self.room, self.bot)
                            self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                        else:
                            self.row = movement.dn(self.row, self.col, self.room, self.bot)
                            if self.room[self.row][self.col+1] == 'w':
                                self.robot_room[self.row][self.col+1] = 'w'
                            if self.room[self.row][self.col-1] == 'w':
                                self.robot_room[self.row][self.col-1] = 'w'
                            self.robot_room[self.row][self.col] = 'k'
                            self.plot(self.row, self.col)

        else:  # Gap Filling
            not_done = Functions.is_unknown_region(self.closest_unknown, self.robot_room)
            if not not_done:
                self.robot_room[self.row][self.col] = 'E'
                Room.print_f(self.robot_room, 'R')
                self.stop()

            elif self.closest_unknown[0] + 1 < self.row:
                    if self.robot_room[self.row - 1][self.col] == 'k':
                        self.row = movement.un(self.row, self.col, self.room, self.bot)
                        self.robot_room[self.row][self.col] = '2k'
                        self.plot(self.row, self.col)
            elif self.closest_unknown[0] != self.row:
                if self.closest_unknown[1] >= self.col:
                    # Obstacle on the Right
                    self.flag = 'r'
                    # Trying to Go Into the Unknown Cell
                    if self.robot_room[self.row-1][self.col] != 'u':
                        if self.robot_room[self.row][self.col+1] == 'k':
                            self.col = movement.rn(self.row, self.col, self.room, self.bot)
                            self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                                self.robot_room[self.row + 1][self.col] = 'w'
                            if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row - 1][self.col] = 'w'
                            if self.room[self.row][self.col + 1] == 'w' and self.row < len(self.robot_room) - 2:
                                self.robot_room[self.row][self.col + 1] = 'w'
                            if self.room[self.row][self.col - 1] == 'w' and self.row > 1:
                                self.robot_room[self.row][self.col - 1] = 'w'
                    elif self.room[self.row-1][self.col] != 'w':
                        self.row = movement.un(self.row, self.col, self.room, self.bot)
                        self.robot_room[self.row][self.col] = 'k'
                        self.plot(self.row, self.col)
                        # Sensor Checking
                        if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                            self.robot_room[self.row + 1][self.col] = 'w'
                        if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                            self.robot_room[self.row - 1][self.col] = 'w'
                        if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room)-2:
                            self.robot_room[self.row][self.col+1] = 'w'
                        if self.room[self.row][self.col-1] == 'w' and self.row > 1:
                            self.robot_room[self.row][self.col-1] = 'w'

                elif self.closest_unknown[1] < self.col:
                    # Obstacle on the Left
                    self.flag = 'l'
                    # Trying to Go Into the Unknown Cell
                    if self.robot_room[self.row - 1][self.col] != 'u':
                        if self.robot_room[self.row][self.col - 1] == 'k':
                            self.col = movement.ln(self.row, self.col, self.room, self.bot)
                            self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                                self.robot_room[self.row + 1][self.col] = 'w'
                            if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row - 1][self.col] = 'w'
                            if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room)-2:
                                self.robot_room[self.row][self.col+1] = 'w'
                            if self.room[self.row][self.col-1] == 'w' and self.row > 1:
                                self.robot_room[self.row][self.col-1] = 'w'
                    elif self.room[self.row - 1][self.col] != 'w':
                        self.row = movement.un(self.row, self.col, self.room, self.bot)
                        self.robot_room[self.row][self.col] = 'k'
                        self.plot(self.row, self.col)
                        # Sensor Checking
                        if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                            self.robot_room[self.row + 1][self.col] = 'w'
                        if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                            self.robot_room[self.row - 1][self.col] = 'w'
                        if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room)-2:
                            self.robot_room[self.row][self.col+1] = 'w'
                        if self.room[self.row][self.col-1] == 'w' and self.row > 1:
                            self.robot_room[self.row][self.col-1] = 'w'

            elif self.closest_unknown[0] == self.row:
                # If Unknown On Same Row
                if self.robot_room[self.row][self.col+1] == 'u':
                    if self.room[self.row][self.col+1] != 'w':
                        self.col = movement.rn(self.row, self.col, self.room, self.bot)
                        if self.robot_room[self.row][self.col] == 'u':
                            self.robot_room[self.row][self.col] = 'k'
                        elif self.robot_room[self.row][self.col] == 'k':
                            self.robot_room[self.row][self.col] = '2k'
                        self.plot(self.row, self.col)
                        # Sensor Checking
                        if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room)-2:
                            self.robot_room[self.row+1][self.col] = 'w'
                        if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                            self.robot_room[self.row-1][self.col] = 'w'
                        if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room)-2:
                            self.robot_room[self.row][self.col+1] = 'w'
                        if self.room[self.row][self.col-1] == 'w' and self.row > 1:
                            self.robot_room[self.row][self.col-1] = 'w'

                elif self.robot_room[self.row][self.col - 1] == 'u':
                    if self.room[self.row][self.col-1] != 'w':
                        if self.room[self.row][self.col - 1] != 'w':
                            self.col = movement.ln(self.row, self.col, self.room, self.bot)
                            if self.robot_room[self.row][self.col] == 'u':
                                self.robot_room[self.row][self.col] = 'k'
                            elif self.robot_room[self.row][self.col] == 'k':
                                self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                                self.robot_room[self.row + 1][self.col] = 'w'
                            if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row - 1][self.col] = 'w'
                            if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room)-2:
                                self.robot_room[self.row][self.col+1] = 'w'
                            if self.room[self.row][self.col-1] == 'w' and self.row > 1:
                                self.robot_room[self.row][self.col-1] = 'w'
            self.closest_unknown.clear()

    def plot(self, row, col):
        length = 10
        width = 10
        with self.canvas:
            if self.robot_room[row][col] != '2k':
                Color(0, 1, 1, 1)
            else:
                Color(0, 0.5, 0.8, 1)
            self.rect = Rectangle(pos=(col*50*(10/width)+5*(10/width),
                                       500-(45*(10/length))-row*50*(10/length)),
                                  size=(40*(10/width), 40*(10/length)))

    def set_room_canvas(self, **kwargs):
        length = 10
        width = 10
        for i in range(length):
            with self.canvas:
                Color(0.5, 0.5, 0.5, 1)
                self.rect = Rectangle(pos=(5, i*50+5), size=(40, 40))
            with self.canvas:
                Color(0.5, 0.5, 0.5, 1)
                self.rect = Rectangle(pos=(5, i*50+5), size=(40, 40))
            if i == 0 or i == length - 1:
                for j in range(1, width):
                    with self.canvas:
                        Color(0.5, 0.5, 0.5, 1)
                        self.rect = Rectangle(pos=(j*50+5, i*50+5), size=(40, 40))
            else:
                for j in range(1, width):
                    if j != width - 1:
                        pass
                    else:
                        with self.canvas:
                            Color(0.5, 0.5, 0.5, 1)
                            self.rect = Rectangle(pos=(j * 50 + 5, i * 50 + 5), size=(40, 40))

    def set_room(self, **kwargs):
        length = 10
        width = 10
        for i in range(length):
            self.room.append(['w'])
            self.robot_room.append(['w'])
            if i == 0 or i == length-1:
                for j in range(1, width):
                    self.room[i].append('w')
                    self.robot_room[i].append('w')
            else:
                for j in range(1, width-1):
                    self.room[i].append(' ')
                    self.robot_room[i].append(' ')
                self.room[i].append('w')
                self.robot_room[i].append('w')
        for rows in range(1, len(self.robot_room)-1):
            for cell in range(1, len(self.robot_room[rows])-1):
                self.robot_room[rows][cell] = 'u'
        self.obstacle()
        self.row = 1
        self.col = 1
        self.room[self.row][self.col] = self.bot
        self.robot_room[self.row][self.col] = 'S'
        self.plot(1, 1)
        Room.print_f(self.room, 'R')
        print('\n')

    def obstacle(self, obs_row=3, obs_col=3, obs_hei=4, obs_wid=4):
        obstacle_point = [obs_row, obs_col]
        obstacle_size = [obs_hei, obs_wid]
        if obstacle_point[0] <= (len(self.room)-1) and obstacle_point[1] <= (len(self.room[0])-1):
            if (obstacle_point[0] + obstacle_size[0] <= (len(self.room)-1)
                    and obstacle_point[1] + obstacle_size[1] <= (len(self.room[0])-1)):
                for x in range(obstacle_point[0], obstacle_point[0] + obstacle_size[0]):
                    for y in range(obstacle_point[1], obstacle_point[1] + obstacle_size[1]):
                        if self.room[x][y] != 'w':
                            self.room[x][y] = 'w'
                            with self.canvas:
                                Color(0.5, 0.5, 0.5, 1)
                                self.rect = Rectangle(pos=(x*50+5, y*50+5), size=(40, 40))

    def clear_room(self):
        self.room.clear()
        self.robot_room.clear()
        self.flag = 'r'
        self.bot = 'b'
        self.row = 0
        self.col = 0
        with self.canvas:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=(0, 0), size=(500, 500))


class SizeSelect(Screen):

    height_def = ObjectProperty()
    width_def = ObjectProperty()
    obs_row_def = ObjectProperty()
    obs_col_def = ObjectProperty()
    obs_height_def = ObjectProperty()
    obs_width_def = ObjectProperty()
    obs_row = 0
    obs_col = 0
    obs_hei = 0
    obs_wid = 0
    room = []
    robot_room = []
    closest_unknown = []
    done_gap_filling = False
    done_region_filling = False
    flag = 'r'
    bot = 'b'
    row = 0
    col = 0
    room_length = 0
    room_width = 0
    before_obstacle = True
    obs_bypass = False
    last_filling = False
    obs_last_row =False

    def go(self, **kwargs):
        super(SizeSelect, self).__init__(**kwargs)
        Clock.schedule_interval(self.start, 0.05)

    def stop(self):
        Clock.unschedule(self.start)

    def start(self, *args):
        #  Region Filling
        if not self.done_region_filling:

            if Functions.been_in_row(self.robot_room) and not self.obs_last_row:
                self.done_region_filling = True

            elif self.room[self.row][self.col+1] != 'w' and self.flag == 'r'\
                    and self.robot_room[self.row][self.col+1] != 'k':
                # Right Movement
                if self.robot_room[1][2] == 'u':
                    if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                        self.robot_room[self.row + 1][self.col] = 'w'
                    if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                        self.robot_room[self.row - 1][self.col] = 'w'
                self.col = movement.rn(self.row, self.col, self.room, self.bot)
                if self.room[self.row][self.col + 1] == 'w' and self.col <= len(self.robot_room) - 2:
                    self.robot_room[self.row][self.col + 1] = 'w'
                if self.room[self.row][self.col - 1] == 'w' and self.col > 1:
                    self.robot_room[self.row][self.col - 1] = 'w'
                if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                    self.robot_room[self.row + 1][self.col] = 'w'
                if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                    self.robot_room[self.row - 1][self.col] = 'w'
                self.robot_room[self.row][self.col] = 'k'
                self.plot(self.row, self.col)

            elif self.room[self.row][self.col-1] != 'w' and self.flag == 'l'\
                    and self.robot_room[self.row][self.col-1] != 'k':
                # Left Movement
                self.col = movement.ln(self.row, self.col, self.room, self.bot)
                if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                    self.robot_room[self.row+1][self.col] = 'w'
                if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                    self.robot_room[self.row-1][self.col] = 'w'
                self.robot_room[self.row][self.col] = 'k'
                self.plot(self.row, self.col)

            elif (self.room[self.row][self.col+1] == 'w' or self.robot_room[self.row][self.col+1] == 'k'
                    or self.robot_room[self.row][self.col+1] == '2k') and self.flag == 'r':
                # Obstacle
                if self.col < (len(self.robot_room[self.row])-2) and self.room[self.row][self.col+1] == 'w':
                    self.robot_room[self.row][self.col+1] = 'w'
                if self.room[self.row][self.col+1] == 'w':
                    self.flag = 'l'
                # 90 Deg to the Right
                if self.room[self.row+1][self.col] != 'w' and self.room[self.row+1][self.col] != 'k':
                    if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                        self.robot_room[self.row-1][self.col] = 'w'
                    self.row = movement.dn(self.row, self.col, self.room, self.bot)
                    self.robot_room[self.row][self.col] = 'k'
                    self.plot(self.row, self.col)
                    if self.room[self.row][self.col+1] == 'w' and self.col <= len(self.robot_room)-2:
                        self.robot_room[self.row][self.col + 1] = 'w'
                    if self.room[self.row][self.col-1] == 'w':
                        self.robot_room[self.row][self.col-1] = 'w'
                    if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                        self.robot_room[self.row + 1][self.col] = 'w'
                    if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                        self.robot_room[self.row - 1][self.col] = 'w'

                else:  # Dead Lock - Reverse
                    if self.robot_room[self.row][self.col] == 'k':
                        self.flag = 'l'
                        if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room)-2:
                            self.robot_room[self.row+1][self.col] = 'w'
                        if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                            self.robot_room[self.row-1][self.col] = 'w'
                        if not(Functions.been_in_row(self.robot_room)):
                            if self.room[self.row+1][self.col] == 'w':
                                self.robot_room[self.row+1][self.col] = 'w'
                            self.col = movement.ln(self.row, self.col, self.room, self.bot)
                            if self.robot_room[self.row][self.col] == 'k':
                                self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                    else:
                        self.col = movement.rn(self.row, self.col, self.room, self.bot)
                        if self.robot_room[self.row][self.col] == 'k':
                            self.robot_room[self.row][self.col] = '2k'
                        self.plot(self.row, self.col)

            elif (self.room[self.row][self.col-1] == 'w' or self.robot_room[self.row][self.col-11] == 'k'
                  or self.robot_room[self.row][self.col+1] == '2k') and self.flag == 'l':
                # Obstacle
                if self.col > 1 and self.room[self.row][self.col-1] == 'w':
                    self.robot_room[self.row][self.col-1] = 'w'
                if self.room[self.row][self.col-1] == 'w':
                    self.flag = 'r'
                # 90 Deg to the Left
                if self.room[self.row+1][self.col] != 'w':
                    if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                        self.robot_room[self.row-1][self.col] = 'w'
                    self.row = movement.dn(self.row, self.col, self.room, self.bot)
                    self.robot_room[self.row][self.col] = 'k'
                    self.plot(self.row, self.col)
                    if self.room[self.row][self.col+1] == 'w':
                        self.robot_room[self.row][self.col + 1] = 'w'
                    if self.room[self.row][self.col-1] == 'w':
                        self.robot_room[self.row][self.col - 1] = 'w'
                        self.obs_last_row = True
                    if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                        self.robot_room[self.row + 1][self.col] = 'w'
                    if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                        self.robot_room[self.row - 1][self.col] = 'w'

                else:  # Dead Lock - Reverse
                    if self.robot_room[self.row][self.col] == 'k':
                        self.flag = 'r'
                        if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                            self.robot_room[self.row+1][self.col] = 'w'
                        if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                            self.robot_room[self.row-1][self.col] = 'w'
                        if not (Functions.been_in_row(self.robot_room)):
                            self.col = movement.rn(self.row, self.col, self.room, self.bot)
                            if self.robot_room[self.row][self.col] == 'k':
                                self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                    else:
                        self.col = movement.ln(self.row, self.col, self.room, self.bot)
                        if self.robot_room[self.row][self.col] == 'k':
                            self.robot_room[self.row][self.col] = '2k'
                        self.plot(self.row, self.col)

            if self.robot_room[len(self.robot_room)-2][len(self.robot_room[len(self.robot_room)-2])-2] != 'u'\
                    or self.robot_room[len(self.robot_room) - 2][1] != 'u':
                self.obs_last_row = False

        else:  # Gap Filling
            not_done = Functions.is_unknown_region(self.closest_unknown, self.robot_room)
            if not not_done:
                self.robot_room[self.row][self.col] = 'E'
                Room.print_f(self.robot_room, 'R')
                self.stop()

            elif self.closest_unknown[0] + 1 < self.row:
                # Getting to Line Beneath the unknown area
                    if self.robot_room[self.row - 1][self.col] == 'k':
                        self.row = movement.un(self.row, self.col, self.room, self.bot)
                        if self.robot_room[self.row][self.col] == 'u':
                            self.robot_room[self.row][self.col] = 'k'
                        elif self.robot_room[self.row][self.col] == 'k':
                            self.robot_room[self.row][self.col] = '2k'
                    elif self.robot_room[self.row - 1][self.col] == 'w':
                        if self.closest_unknown[1] > self.col:
                            if self.robot_room[self.row][self.col+1] == 'k':
                                self.col = movement.rn(self.row, self.col, self.room, self.bot)
                                if self.robot_room[self.row][self.col] == 'u':
                                    self.robot_room[self.row][self.col] = 'k'
                                elif self.robot_room[self.row][self.col] == 'k':
                                    self.robot_room[self.row][self.col] = '2k'
                        elif self.closest_unknown[1] < self.col:
                            self.col = movement.ln(self.row, self.col, self.room, self.bot)
                            if self.robot_room[self.row][self.col] == 'u':
                                self.robot_room[self.row][self.col] = 'k'
                            elif self.robot_room[self.row][self.col] == 'k':
                                self.robot_room[self.row][self.col] = '2k'
                    self.plot(self.row, self.col)
            elif self.closest_unknown[0] < self.row:
                if self.closest_unknown[1] >= self.col:
                    # Unknown on the Right
                    self.flag = 'r'
                    # Trying to Go Into the Unknown Cell
                    if self.robot_room[self.row-1][self.col] != 'u':
                        if self.robot_room[self.row][self.col+1] == 'k':
                            self.col = movement.rn(self.row, self.col, self.room, self.bot)
                            self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                                self.robot_room[self.row + 1][self.col] = 'w'
                            if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row - 1][self.col] = 'w'
                            if self.room[self.row][self.col + 1] == 'w' and self.row < len(self.robot_room) - 2:
                                self.robot_room[self.row][self.col + 1] = 'w'
                            if self.room[self.row][self.col - 1] == 'w' and self.row > 1:
                                self.robot_room[self.row][self.col - 1] = 'w'
                    elif self.room[self.row-1][self.col] != 'w':
                        self.row = movement.un(self.row, self.col, self.room, self.bot)
                        self.robot_room[self.row][self.col] = 'k'
                        self.plot(self.row, self.col)
                        # Sensor Checking
                        if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                            self.robot_room[self.row + 1][self.col] = 'w'
                        if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                            self.robot_room[self.row - 1][self.col] = 'w'
                        if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room)-2:
                            self.robot_room[self.row][self.col+1] = 'w'
                        if self.room[self.row][self.col-1] == 'w' and self.row > 1:
                            self.robot_room[self.row][self.col-1] = 'w'

                elif self.closest_unknown[1] < self.col:
                    # Unknown on the Left
                    self.flag = 'l'
                    # Trying to Go Into the Unknown Cell
                    if self.robot_room[self.row - 1][self.col] != 'u':
                        if self.robot_room[self.row][self.col - 1] == 'k':
                            self.col = movement.ln(self.row, self.col, self.room, self.bot)
                            self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                                self.robot_room[self.row + 1][self.col] = 'w'
                            if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row - 1][self.col] = 'w'
                            if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room)-2:
                                self.robot_room[self.row][self.col+1] = 'w'
                            if self.room[self.row][self.col-1] == 'w' and self.row > 1:
                                self.robot_room[self.row][self.col-1] = 'w'
                    elif self.room[self.row - 1][self.col] != 'w':
                        self.row = movement.un(self.row, self.col, self.room, self.bot)
                        self.robot_room[self.row][self.col] = 'k'
                        self.plot(self.row, self.col)
                        # Sensor Checking
                        if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                            self.robot_room[self.row + 1][self.col] = 'w'
                        if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                            self.robot_room[self.row - 1][self.col] = 'w'
                        if self.room[self.row][self.col+1] == 'w' and self.col < len(self.robot_room)-2:
                            self.robot_room[self.row][self.col+1] = 'w'
                        if self.room[self.row][self.col-1] == 'w' and self.col > 1:
                            self.robot_room[self.row][self.col-1] = 'w'

            elif self.closest_unknown[0] >= self.row:
                if self.closest_unknown[0] == self.row:
                    # If Unknown On Same Row
                    if self.closest_unknown[1] > self.col:
                        if self.room[self.row][self.col+1] != 'w':
                            if self.robot_room[self.row][self.col+1] == 'u':
                                self.col = movement.rn(self.row, self.col, self.room, self.bot)
                                self.robot_room[self.row][self.col] = 'k'
                            elif self.robot_room[self.row][self.col+1] == 'k':
                                self.col = movement.rn(self.row, self.col, self.room, self.bot)
                                self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room)-2:
                                self.robot_room[self.row+1][self.col] = 'w'
                            if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row-1][self.col] = 'w'
                            if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room)-2:
                                self.robot_room[self.row][self.col+1] = 'w'
                            if self.room[self.row][self.col-1] == 'w' and self.row > 1:
                                self.robot_room[self.row][self.col-1] = 'w'
                        else:
                            self.robot_room[self.row][self.col + 1] = 'w'
                            if Functions.is_unknown_region(self.closest_unknown, self.robot_room):
                                self.row = movement.un(self.row, self.col, self.room, self.bot)
                                if self.robot_room[self.row][self.col] == 'u':
                                    self.robot_room[self.row][self.col] = 'k'
                                elif self.robot_room[self.row][self.col] == 'k':
                                    self.robot_room[self.row][self.col] = '2k'
                                self.plot(self.row, self.col)

                    elif self.closest_unknown[1] < self.col:
                        if self.room[self.row][self.col-1] != 'w':
                            if self.robot_room[self.row][self.col-1] == 'u':
                                self.col = movement.ln(self.row, self.col, self.room, self.bot)
                                self.robot_room[self.row][self.col] = 'k'
                            elif self.robot_room[self.row][self.col-1] == 'k':
                                self.col = movement.ln(self.row, self.col, self.room, self.bot)
                                self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room)-2:
                                self.robot_room[self.row+1][self.col] = 'w'
                            if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row-1][self.col] = 'w'
                            if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room)-2:
                                self.robot_room[self.row][self.col+1] = 'w'
                            if self.room[self.row][self.col-1] == 'w' and self.row > 1:
                                self.robot_room[self.row][self.col-1] = 'w'
                        else:
                            self.robot_room[self.row][self.col - 1] = 'w'
                            if Functions.is_unknown_region(self.closest_unknown, self.robot_room):
                                self.row = movement.un(self.row, self.col, self.room, self.bot)
                                if self.robot_room[self.row][self.col] == 'u':
                                    self.robot_room[self.row][self.col] = 'k'
                                elif self.robot_room[self.row][self.col] == 'k':
                                    self.robot_room[self.row][self.col] = '2k'
                                self.plot(self.row, self.col)

                elif self.closest_unknown[0] > self.row:
                    if self.closest_unknown[1] > self.col:
                        if self.room[self.row][self.col+1] == 'w'\
                                and self.col < len(self.robot_room[self.col])-1 and self.before_obstacle:
                            # see if still obstacle on the right
                            self.robot_room[self.row][self.col + 1] = 'w'
                            self.row = movement.un(self.row, self.col, self.room, self.bot)
                            if self.robot_room[self.row][self.col] == 'u':
                                self.robot_room[self.row][self.col] = 'k'
                            elif self.robot_room[self.row][self.col] == 'k':
                                self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room)-2:
                                self.robot_room[self.row+1][self.col] = 'w'
                            if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row - 1][self.col] = 'w'
                            if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room[self.col])-1:
                                self.robot_room[self.row][self.col + 1] = 'w'
                            else:
                                self.before_obstacle = False
                                self.obs_bypass = True
                            if self.room[self.row][self.col - 1] == 'w' and self.col > 1:
                                self.robot_room[self.row][self.col - 1] = 'w'

                        elif self.room[self.row][self.col + 1] != 'w' \
                                and self.col < len(self.robot_room[self.col])-1 and self.obs_bypass:
                            if self.robot_room[self.row][self.col + 1] == 'u':
                                self.col = movement.rn(self.row, self.col, self.room, self.bot)
                                self.robot_room[self.row][self.col] = 'k'
                            elif self.robot_room[self.row][self.col + 1] == 'k':
                                self.col = movement.rn(self.row, self.col, self.room, self.bot)
                                self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                                self.robot_room[self.row + 1][self.col] = 'w'
                            if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row - 1][self.col] = 'w'
                            if self.room[self.row][self.col + 1] == 'w'\
                                    and self.row < len(self.robot_room[self.col]) - 1:
                                self.robot_room[self.row][self.col + 1] = 'w'
                            if self.room[self.row][self.col - 1] == 'w' and self.col > 1:
                                self.robot_room[self.row][self.col - 1] = 'w'

                            if self.robot_room[self.row+1][self.col] == 'w':
                                for i in range(self.row+1, len(self.robot_room)-1):
                                    self.robot_room[i][self.col] = 'w'
                            else:
                                self.obs_bypass = False
                                self.before_obstacle = False

                    elif self.closest_unknown[1] < self.col:
                        if self.room[self.row][self.col-1] == 'w'\
                                and self.col > 1 and self.before_obstacle:
                            # see if still obstacle on the right
                            self.robot_room[self.row][self.col - 1] = 'w'
                            self.row = movement.un(self.row, self.col, self.room, self.bot)
                            if self.robot_room[self.row][self.col] == 'u':
                                self.robot_room[self.row][self.col] = 'k'
                            elif self.robot_room[self.row][self.col] == 'k':
                                self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row+1][self.col] == 'w' and self.row < len(self.robot_room)-2:
                                self.robot_room[self.row+1][self.col] = 'w'
                            if self.room[self.row-1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row - 1][self.col] = 'w'
                            if self.room[self.row][self.col+1] == 'w' and self.row < len(self.robot_room[self.col])-1:
                                self.robot_room[self.row][self.col + 1] = 'w'
                            if self.room[self.row][self.col - 1] == 'w' and self.col > 1:
                                self.robot_room[self.row][self.col - 1] = 'w'
                            else:
                                self.before_obstacle = False
                                self.obs_bypass = True

                        elif self.room[self.row][self.col - 1] != 'w' \
                                and self.col > 1 and self.obs_bypass:
                            if self.robot_room[self.row][self.col - 1] == 'u':
                                self.col = movement.ln(self.row, self.col, self.room, self.bot)
                                self.robot_room[self.row][self.col] = 'k'
                            elif self.robot_room[self.row][self.col - 1] == 'k':
                                self.col = movement.ln(self.row, self.col, self.room, self.bot)
                                self.robot_room[self.row][self.col] = '2k'
                            self.plot(self.row, self.col)
                            # Sensor Checking
                            if self.room[self.row + 1][self.col] == 'w' and self.row < len(self.robot_room) - 2:
                                self.robot_room[self.row + 1][self.col] = 'w'
                            if self.room[self.row - 1][self.col] == 'w' and self.row > 1:
                                self.robot_room[self.row - 1][self.col] = 'w'
                            if self.room[self.row][self.col + 1] == 'w'\
                                    and self.row < len(self.robot_room[self.col]) - 1:
                                self.robot_room[self.row][self.col + 1] = 'w'
                            if self.room[self.row][self.col - 1] == 'w' and self.col > 1:
                                self.robot_room[self.row][self.col - 1] = 'w'

                            if self.robot_room[self.row+1][self.col] == 'w':
                                for i in range(self.row+1, len(self.robot_room)-1):
                                    self.robot_room[i][self.col] = 'w'
                            else:
                                self.obs_bypass = False
                                self.before_obstacle = False
                                self.flag = 'l'

                        elif not self.obs_bypass and not self.before_obstacle and self.flag == 'l':
                            self.last_filling = True
                            self.row = movement.dn(self.row, self.col, self.room, self.bot)
                            self.robot_room[self.row][self.col] = 'k'
                            self.plot(self.row, self.col)

                    elif self.closest_unknown[1] == self.col:
                        if not self.obs_bypass and not self.before_obstacle:
                            self.last_filling = True
                            self.row = movement.dn(self.row, self.col, self.room, self.bot)
                            self.robot_room[self.row][self.col] = 'k'
                            self.plot(self.row, self.col)

    def plot(self, row, col):
        with self.canvas:
            if self.robot_room[row][col] != '2k':
                Color(0, 1, 1, 1)
            else:
                Color(0, 0.5, 0.8, 1)
            self.rect = Rectangle(pos=(col*50*(10/self.room_width)+5*(10/self.room_width),
                                       500-(45*(10/self.room_length))-row*50*(10/self.room_length)),
                                  size=(40*(10/self.room_width), 40*(10/self.room_length)))

    def obstacle_list(self):
        self.obs_row = (int(self.obs_row_def.text))
        self.obs_col = (int(self.obs_col_def.text))
        self.obs_hei = (int(self.obs_height_def.text))
        self.obs_wid = (int(self.obs_width_def.text))
        self.set_obstacle(self.obs_row, self.obs_col, self.obs_hei, self.obs_wid)
        self.set_obstacle_canvas(self.obs_row, self.obs_col, self.obs_hei, self.obs_wid)
        print(self.obs_row, ' ', self.obs_col, ' ', self.obs_hei, ' ', self.obs_wid)

    def set_obstacle(self, obs_row=3, obs_col=3, obs_hei=4, obs_wid=4):
        obstacle_point = [obs_row, obs_col]
        obstacle_size = [obs_hei, obs_wid]
        if obstacle_point[0] <= (len(self.room) - 1) and obstacle_point[1] <= (len(self.room[0]) - 1):
            if (obstacle_point[0] + obstacle_size[0] <= (len(self.room) - 1)
                    and obstacle_point[1] + obstacle_size[1] <= (len(self.room[0]) - 1)):
                for x in range(obstacle_point[0], obstacle_point[0] + obstacle_size[0]):
                    for y in range(obstacle_point[1], obstacle_point[1] + obstacle_size[1]):
                        if self.room[x][y] != 'w':
                            self.room[x][y] = 'w'

    def set_obstacle_canvas(self, obs_row=3, obs_col=3, obs_hei=4, obs_wid=4):
        self.room_length = int(self.height_def.text)
        self.room_width = int(self.width_def.text)
        obstacle_point = [obs_row, obs_col]
        obstacle_size = [obs_hei, obs_wid]
        if obstacle_point[0] <= (len(self.room) - 1) and obstacle_point[1] <= (len(self.room[0]) - 1):
            if (obstacle_point[0] + obstacle_size[0] <= (len(self.room) - 1)
                    and obstacle_point[1] + obstacle_size[1] <= (len(self.room[0]) - 1)):
                for x in range(obstacle_point[1], obstacle_point[1] + obstacle_size[1]):
                    for y in range(self.room_length - 1 - obstacle_point[0],
                                   self.room_length-1-obstacle_point[0]-obstacle_size[0], - 1):
                        with self.canvas:
                            Color(0.5, 0.5, 0.5, 1)
                            self.rect = Rectangle(pos=(x * 50*(10/self.room_width) + 5*(10/self.room_width),
                                                       y * 50*(10/self.room_length) + 5*(10/self.room_length)),
                                                  size=(40*(10/self.room_width), 40*(10/self.room_length)))
        Room.print_f(self.room, 'R')

    def set_room(self, **kwargs):
        self.room_length = int(self.height_def.text)
        self.room_width = int(self.width_def.text)
        for i in range(self.room_length):
            self.room.append(['w'])
            self.robot_room.append(['w'])
            if i == 0 or i == self.room_length - 1:
                for j in range(1, self.room_width):
                    self.room[i].append('w')
                    self.robot_room[i].append('w')
            else:
                for j in range(1, self.room_width - 1):
                    self.room[i].append(' ')
                    self.robot_room[i].append(' ')
                self.room[i].append('w')
                self.robot_room[i].append('w')
        for rows in range(1, len(self.robot_room) - 1):
            for cell in range(1, len(self.robot_room[rows]) - 1):
                self.robot_room[rows][cell] = 'u'
        self.row = 1
        self.col = 1
        self.room[self.row][self.col] = self.bot
        self.robot_room[self.row][self.col] = 'S'
        self.plot(1, 1)
        Room.print_f(self.room, 'R')

    def set_room_canvas(self, **kwargs):
        for i in range(self.room_length):
            with self.canvas:
                Color(0.5, 0.5, 0.5, 1)
                self.rect = Rectangle(pos=(5*(10/self.room_width), i * 50*(10/self.room_length) + (10/self.room_length)*5),
                                      size=(((10/self.room_width)*40), ((10/self.room_length)*40)))
            if i == 0 or i == self.room_length - 1:
                for j in range(1, self.room_width):
                    with self.canvas:
                        Color(0.5, 0.5, 0.5, 1)
                        self.rect = Rectangle(pos=(j * 50*(10/self.room_width) + 5*(10/self.room_width),
                                                   i * 50*(10/self.room_length) + 5*(10/self.room_length)),
                                              size=(((10/self.room_width)*40), ((10/self.room_length)*40)))
            else:
                for j in range(1, self.room_width):
                    if j != self.room_width - 1:
                        pass
                    else:
                        with self.canvas:
                            Color(0.5, 0.5, 0.5, 1)
                            self.rect = Rectangle(pos=(j * 50*(10/self.room_width) + 5*(10/self.room_width),
                                                       i * 50*(10/self.room_length) + 5*(10/self.room_length)),
                                                  size=(40*(10/self.room_width), 40*(10/self.room_length)))

    def clear_room(self):
        self.obs_row = 0
        self.obs_col = 0
        self.obs_hei = 0
        self.obs_wid = 0
        self.room.clear()
        self.robot_room.clear()
        self.closest_unknown.clear()
        self.done_gap_filling = False
        self. done_region_filling = False
        self. flag = 'r'
        self.bot = 'b'
        self.row = 0
        self.col = 0
        self.room_length = 0
        self.room_width = 0
        with self.canvas:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=(0, 0), size=(500, 500))


presentation = Builder.load_file("OpenScreen.kv")


class MainApp(App):
    def build(self):
        return presentation


if __name__ == "__main__":
    MainApp().run()

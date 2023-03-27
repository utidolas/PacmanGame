import pygame
from abc import ABCMeta, abstractmethod
import random

pygame.init()

# Fonts var
arial_font = pygame.font.SysFont("arial", 48, True, False)

# Colors var
yellow_color = (227, 224, 18)
black_color = (0, 0, 0)
blue_color = (0, 0, 255)
red_color = (255, 0, 0)
white_color = (255, 255, 255)
cyan_color = (0, 247, 255)
orange_color = (255, 140, 0)
pink_color = (255, 0, 255)

# Char var
char_speed = 1

# Ghost var/const
RIGHT = 1
UP = 2
LEFT = 3
DOWN = 4

# Room/screen var
room_width = 1280
room_height = 720
game_screen = pygame.display.set_mode((room_width, room_height), 0)


# abstracting common game's elements
class GameElements(metaclass=ABCMeta):
    @abstractmethod
    def paint(self, screen):
        pass

    @abstractmethod
    def computing_rules(self):
        pass

    @abstractmethod
    def processing_events(self, evts):
        pass


class CanMove(metaclass=ABCMeta):
    @abstractmethod
    def approve_movement(self):
        pass

    @abstractmethod
    def disapprove_movement(self, directions):
        pass

    @abstractmethod
    def corner(self, directions):
        pass


class Scenario(GameElements):
    def __init__(self, size, pac):
        self.pacman = pac
        self.canmoves = []
        # Game States 0-Playing, 1-Paused, 2-GameOver, 3-Victory
        self.state = "Playing"
        self.size = size
        self.lives = 5
        self.points = 0

        # 2 = Wall, 1 = FreeSpace
        self.matrix = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def add_movable(self, obj):
        self.canmoves.append(obj)

    def paint_score(self, screen):
        points_x = 30 * self.size
        img_points = arial_font.render("Score: {}".format(self.points), True, yellow_color)
        img_lives = arial_font.render("Lives: {}".format(self.lives), True, yellow_color)
        screen.blit(img_points, (points_x, 50))
        screen.blit(img_lives, (points_x, 100))

    def paint_line(self, screen, line_number, line):
        # counting column and giving them their resp. values
        for column_number, column in enumerate(line):
            x = column_number * self.size
            y = line_number * self.size
            half = self.size // 2
            color = black_color

            # drawing points and walls
            if column == 2:
                color = blue_color
            pygame.draw.rect(screen, color, (x, y, self.size, self.size), 0)
            if column == 1:
                pygame.draw.circle(screen, yellow_color, (x + half, y + half), self.size // 8, 0)

    # actually painting
    def paint(self, screen):
        if self.state == "Playing":
            self.paint_playing(screen)
        elif self.state == "Paused":
            self.paint_playing(screen)
            self.paint_paused(screen)
        elif self.state == "GameOver":
            self.paint_playing(screen)
            self.paint_gameover(screen)
        elif self.state == "Victory":
            self.paint_playing(screen)
            self.paint_victory(screen)

    def paint_text_center(self, screen, text):
        text_img = arial_font.render(text, True, yellow_color)
        text_x = (screen.get_width() - text_img.get_width()) // 2
        text_y = (screen.get_height() - text_img.get_height()) // 2
        screen.blit(text_img, (text_x, text_y))

    def paint_victory(self, screen):
        self.paint_text_center(screen, "V I C T O R Y :D")

    def paint_gameover(self, screen):
        self.paint_text_center(screen, "G A M E  O V E R")

    def paint_paused(self, screen):
        self.paint_text_center(screen, "P A U S E D")

    def paint_playing(self, screen):
        for line_number, line in enumerate(self.matrix):
            self.paint_line(screen, line_number, line)
        self.paint_score(screen)

    def get_directions(self, line, column):
        directons = []
        if self.matrix[int(line)][int(column + 1)] != 2:
            directons.append(RIGHT)
        if self.matrix[int(line - 1)][int(column)] != 2:
            directons.append(UP)
        if self.matrix[int(line)][int(column - 1)] != 2:
            directons.append(LEFT)
        if self.matrix[int(line + 1)][int(column)] != 2:
            directons.append(DOWN)
        return directons

    def computing_rules(self):
        if self.state == "Playing":
            self.computing_rules_playing()
        elif self.state == "Paused":
            self.computing_rules_paused()
        elif self.state == "GameOver":
            self.computing_rules_gameover()

    def computing_rules_gameover(self):
        pass

    def computing_rules_paused(self):
        pass

    def computing_rules_playing(self):
        # Collisions
        for canmove in self.canmoves:
            line = int(canmove.line)
            column = int(canmove.column)
            line_intention = int(canmove.line_intention)
            column_intention = int(canmove.column_intention)
            directions = self.get_directions(line, column)
            if len(directions) >= 3 :
                canmove.corner(directions)
            if isinstance(canmove, Ghost) and canmove.line == self.pacman.line and canmove.column == self.pacman.column:
                self.lives -= 1
                if self.lives <= 0:
                    self.state = "GameOver"
                else:
                    self.pacman.line = 1
                    self.pacman.column = 1
            else:
                if 0 <= column_intention < 28 and 0 <= line_intention < 29 and self.matrix[line_intention][column_intention] != 2:
                    canmove.approve_movement()
                    if isinstance(canmove, Pacman) and self.matrix[line][column] == 1:
                        self.points += 1
                        self.matrix[line][column] = 0
                        if self.points >= 306:
                            self.state = "Victory"
                else:
                    canmove.disapprove_movement(directions)

    def processing_events(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.state == "Playing":
                        self.state = "Paused"
                    else:
                        self.state = "Playing"


class Pacman(GameElements, CanMove):
    def __init__(self, size):
        self.column = 1
        self.line = 1
        self.xx = 640
        self.yy = 360
        self.size = size
        self.radius = self.size // 2
        self.xspd = 0
        self.yspd = 0
        self.column_intention = self.column # Making collisions with 'intention'
        self.line_intention = self.line
        self.opening = 0 # Mouth animation
        self.openingspd = 1

    def computing_rules(self):
        self.column_intention = self.column + self.xspd # Storing in 'column_intention' to make collision
        self.xx = int(self.column * self.size + self.radius)

        self.line_intention = self.line + self.yspd
        self.yy = int(self.line * self.size + self.radius)

    def approve_movement(self):
        self.line = self.line_intention
        self.column = self.column_intention

    def disapprove_movement(self, directions):
        self.line_intention = self.line
        self.column_intention = self.column

    def corner(self, directions):
        pass


    def paint(self, screen):
        # drawing pacman's body
        pygame.draw.circle(screen, yellow_color, (self.xx, self.yy), self.radius, 0)

        self.opening += self.openingspd
        if self.opening > self.radius:
            self.openingspd = -1
        if self.opening <= 0:
            self.openingspd = 1

        # setting and drawing mouth
        edge1 = (self.xx, self.yy)
        edge2 = (self.xx + self.radius, self.yy - self.opening)
        edge3 = (self.xx + self.radius, self.yy + self.opening)
        edges = [edge1, edge2, edge3]

        pygame.draw.polygon(screen, black_color, edges, 0)

        # setting and drawing eye
        eyex =  self.xx + self.radius // 4
        eyey = self.yy - self.radius // 1.5
        eye_radius = self.radius // 6

        pygame.draw.circle(screen, black_color,(eyex, eyey), eye_radius, 0)

    def processing_events(self, evts):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.xspd = char_speed
                elif e.key == pygame.K_UP:
                    self.yspd = -char_speed
                elif e.key == pygame.K_LEFT:
                    self.xspd = -char_speed
                elif e.key == pygame.K_DOWN:
                    self.yspd = char_speed
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.xspd = 0
                elif e.key == pygame.K_UP:
                    self.yspd = 0
                elif e.key == pygame.K_LEFT:
                    self.xspd = 0
                elif e.key == pygame.K_DOWN:
                    self.yspd = 0


class Ghost(GameElements):
    def __init__(self, color, size):
        self.column = 13
        self.line = 15
        self.line_intention = self.line
        self.column_intention = self.column
        self.speed = 1
        self.direction = DOWN
        self.size = size
        self.color = color


    def paint(self, screen):
        # drawing ghost's body
        slice = self.size // 8
        px = int(self.column * self.size)
        py = int(self.line * self.size)
        outline = [(px, py + self.size),
                   (px + slice, py + slice * 2),
                   (px + slice * 2, py + slice // 2),
                   (px + slice * 3, py),
                   (px + slice * 5, py),
                   (px + slice * 6, py + slice //2),
                   (px + slice * 7, py + slice * 2),
                   (px + self.size, py + self.size)]
        pygame.draw.polygon(screen, self.color, outline, 0)

        # drawing ghost's eyes
        outer_eye_radius = slice
        inner_eye_radius = slice // 1.5
        l_eye_x = int(px + slice * 2.5)
        l_eye_y = int(py + slice * 2.5)
        r_eye_x = int(px + slice * 5.5)
        r_eye_y = int(py + slice * 2.5)

        pygame.draw.circle(screen, white_color, (l_eye_x, l_eye_y), outer_eye_radius, 0)
        pygame.draw.circle(screen, black_color, (l_eye_x, l_eye_y), inner_eye_radius, 0)
        pygame.draw.circle(screen, white_color, (r_eye_x, r_eye_y), outer_eye_radius, 0)
        pygame.draw.circle(screen, black_color, (r_eye_x, r_eye_y), inner_eye_radius, 0)

    def computing_rules(self):
        if self.direction == RIGHT:
            self.column_intention += self.speed
        elif self.direction == UP:
            self.line_intention -= self.speed
        elif self.direction == LEFT:
            self.column_intention -= self.speed
        elif self.direction == DOWN:
            self.line_intention += self.speed

    def change_direction(self, directions):
        self.direction = random.choice(directions)

    def corner(self, directions):
        self.change_direction(directions)

    def approve_movement(self):
        self.line = self.line_intention
        self.column = self.column_intention

    def disapprove_movement(self, directions):
        self.line_intention = self.line
        self.column_intention = self.column
        self.change_direction(directions)

    def processing_events(self, evts):
        pass


if __name__ == "__main__":
    size = room_height // 30
    pacman = Pacman(size)

    # Ghosts
    blinky = Ghost(red_color, size)
    inky = Ghost(cyan_color, size)
    clyde = Ghost(orange_color, size)
    pinky = Ghost(pink_color, size)

    # Scenario
    scenario = Scenario(size, pacman)
    scenario.add_movable(pacman)
    scenario.add_movable(blinky)
    scenario.add_movable(inky)
    scenario.add_movable(clyde)
    scenario.add_movable(pinky)

    while True:
        # rules
        pacman.computing_rules()
        blinky.computing_rules()
        inky.computing_rules()
        clyde.computing_rules()
        pinky.computing_rules()
        scenario.computing_rules()

        # drawing game's elements
        game_screen.fill((black_color))
        scenario.paint(game_screen)
        pacman.paint(game_screen)
        blinky.paint(game_screen)
        inky.paint(game_screen)
        clyde.paint(game_screen)
        pinky.paint(game_screen)
        pygame.display.update()
        pygame.time.delay(100)

        # events
        events = pygame.event.get()
        pacman.processing_events(events)
        scenario.processing_events(events)
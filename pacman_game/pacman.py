from game_character import GameCharacter
# flake8: noqa

"""Problem 1: Pac-Man's chomping"""
# There are two small modifications that must be made to the pacman.py file in
# order to get Pac-Man's mouth working the way it should. You'll need to find
# them both.

"""Problem 3: Eating the dots"""
# To get the dot-eating functionality working, you'll need to make
# modifications in several files. There are TODOs for Problem 3 in pacman.py,
# maze.py, and dots.py. Make sure you understand:
# - How the objects relate to each other in the game. Which object has access
# to which other objects?
# - How the individual dots are displayed, and how the full collection of dots
# is represented within the context of the maze.
# - How the conditions for winning (setting game controller's player_wins
# attribute) are evaluated.
# The places where you'll need to add code are highlighted in the files by the
# TODOs. If you need to add any new instance variables or constants, you
# should put those in an appropriate place in the code.


# The Pacman class extends GameCharacter, so methods defined in GameCharacter
# are inherited by objects of class Pacman.
class Pacman(GameCharacter):
    """Pac Man class"""
    def __init__(self, maze, game_controller):
        self.CHAR_WIDTH = 100
        self.CHAR_HEIGHT = 100
        self.maze = maze
        self.gc = game_controller
        self.x = maze.WIDTH/2
        self.y = maze.BOTTOM_HORIZ
        self.x_add = 0
        self.y_add = 0
        self.max_mouth_angle = 45
        self.min_mouth_angle = 0
        self.mouth_angle = 0
        self.open_close = 0
        self.rot_begin = 0
        self.rot_end = 360
        self.mouth_speed = 5
        self.velocity = 3
        self.WALL_TOLERANCE = 6
        self.MOUTH_RIGHT_BEGIN_ANGLE = 0
        self.MOUTH_RIGHT_END_ANGLE = 360
        self.MOUTH_DOWN_BEGIN_ANGLE = 90
        self.MOUTH_DOWN_END_ANGLE = 450
        self.MOUTH_LEFT_BEGIN_ANGLE = 180
        self.MOUTH_LEFT_END_ANGLE = 540
        self.MOUTH_UP_BEGIN_ANGLE = -90
        self.MOUTH_UP_END_ANGLE = 270

    def draw_self(self, x, y):
        """Draw Pacman's yellow arc shape to screen"""
        noStroke()  # type: ignore
        fill(1.0, 1.0, 0.0)  # type: ignore
        arc(x, y, self.CHAR_WIDTH, self.CHAR_HEIGHT,  # type: ignore
            radians(self.rot_begin + self.mouth_angle),  # type: ignore
            radians(self.rot_end - self.mouth_angle))  # type: ignore

    def update(self):
        """Carry out necessary updates for each frame before
        drawing to screen"""
        self.on_left = (abs(self.x - self.maze.LEFT_VERT) <
                        self.WALL_TOLERANCE)
        self.on_right = (abs(self.x - self.maze.RIGHT_VERT) <
                         self.WALL_TOLERANCE)

        self.on_top = (abs(self.y - self.maze.TOP_HORIZ) <
                       self.WALL_TOLERANCE)
        self.on_bottom = (abs(self.y - self.maze.BOTTOM_HORIZ) <
                          self.WALL_TOLERANCE)

        # if (self.mouth_angle < self.max_mouth_angle):
        #     self.open_close = -(self.mouth_speed)
        # if (self.mouth_angle < self.min_mouth_angle):
        #     self.open_close = self.mouth_speed

        # Flip direction exactly at the limits
        if (self.mouth_angle >= self.max_mouth_angle):
            self.open_close = -(self.mouth_speed)
        if (self.mouth_angle <= self.min_mouth_angle):
            self.open_close = self.mouth_speed

        # If the game is over and Pacman wins, stop moving
        if self.gc.player_wins:
            self.x_add = 0
            self.y_add = 0

        # If the game is over and Pacman loses, top moving and
        # Open mouth to oblivion.
        if self.gc.pinky_wins:
            self.open_close = 1
            self.x_add = 0
            self.y_add = 0

        # Apply mouth & movement update
        self.mouth_angle = self.mouth_angle + self.open_close
        self.x = self.x + self.x_add
        self.y = self.y + self.y_add

        # TODO:
        # PROBLEM 3: implement dot eating
        # PacMan has access to the maze object, which
        # in turn has access to the dots object. Call the
        # eat_dots method on the maze object here.
        # Based on PacMan's location, PacMan should gobble
        # dots from a different list.
        # BEGIN CODE CHANGES
        self.maze.eat_dots(self)
        # END CODE CHANGES

    def control(self, keyCode):
        """Handles keyboard input for PacMan"""
        if (keyCode == DOWN and (self.on_left or self.on_right)):  # type: ignore
            if self.on_left:
                self.x = self.maze.LEFT_VERT
            else:
                self.x = self.maze.RIGHT_VERT
            self.rot_begin = self.MOUTH_DOWN_BEGIN_ANGLE
            self.rot_end = self.MOUTH_DOWN_END_ANGLE
            self.x_add = 0
            self.y_add = self.velocity
        elif (keyCode == UP and (self.on_left or self.on_right)):  # type: ignore
            if self.on_left:
                self.x = self.maze.LEFT_VERT
            else:
                self.x = self.maze.RIGHT_VERT
            self.rot_begin = self.MOUTH_UP_BEGIN_ANGLE
            self.rot_end = self.MOUTH_UP_END_ANGLE
            self.x_add = 0
            self.y_add = -(self.velocity)
        elif (keyCode == LEFT and  # type: ignore
              (self.on_top or self.on_bottom)):
            if self.on_top:
                self.y = self.maze.TOP_HORIZ
            else:
                self.y = self.maze.BOTTOM_HORIZ
            self.rot_begin = self.MOUTH_LEFT_BEGIN_ANGLE
            self.rot_end = self.MOUTH_LEFT_END_ANGLE
            self.x_add = -(self.velocity)
            self.y_add = 0
        elif (keyCode == RIGHT and  # type: ignore
              (self.on_top or self.on_bottom)):
            if self.on_top:
                self.y = self.maze.TOP_HORIZ
            else:
                self.y = self.maze.BOTTOM_HORIZ
            self.rot_begin = self.MOUTH_RIGHT_BEGIN_ANGLE
            self.rot_end = self.MOUTH_RIGHT_END_ANGLE
            self.x_add = self.velocity
            self.y_add = 0

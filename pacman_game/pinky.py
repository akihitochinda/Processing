"""Problem 2: Pinky's AI"""
# At the moment, Pinky is simply moving back and forth along the top
# horizontal corridor. This isn't very exciting "enemy" behavior for a game.
# We'd like to give Pinky some rudimentary AI, so that Pinky chases Pac-Man
# around the maze.

# - Pinky needs to decide which direction to go whenever he is at an
# intersection. Whether he goes up, down, right, or left should depend on
# where Pac-Man is with respect to Pinky.
# - The Processing coordinate space increases along the X axis from left to
# right, and increases along the Y axis from top to bottom. So the upper left
# corner's coordinates are 0, 0 the lower right corner's coordinates (in this
# canvas) are 599, 599.
# - Dividing a number by its absolute value (abs()) is a handy way to isolate
# the number's sign.
# - Pinky's eye movements, as currently implemented, follow the location of
# Pac-Man. Most of the information you'll need to determine which way Pinky
# should go is already being used in some way by the eye movement logic. Read
# that code closely.

# Note on inheritance
# By the way, both Pinky and Pac-Man make use of an object-oriented feature
# that we haven't discussed at length in class: inheritance. Because both
# Pinky and Pac-Man have certain behaviors in common (for example, they both
# need to be drawn twice when overlapping the edge of the screen) I have
# implemented a class called GameCharacter that both Pinky and Pac-Man
# "extend". Take a look at both of those class's class declarations. Notice
# that GameCharacter is there in parentheses. That means that the display()
# method for both the Pinky and Pac-Man classes is inherited from this common
# implementation. You won't be working with this directly, but it's worthwhile
# to know about.

from game_character import GameCharacter
from eyes import Eyes
# flake8: noqa

# The Pinky class extends GameCharacter, so methods defined in GameCharacter
# are inherited by objects of class Pinky.
class Pinky(GameCharacter):
    def __init__(self, maze, pacman, game_controller):
        self.CHAR_WIDTH = 100
        self.CHAR_HEIGHT = 100
        self.maze = maze
        self.pacman = pacman
        self.gc = game_controller
        self.x = maze.WIDTH/2
        self.y = maze.TOP_HORIZ
        self.velocity = 2
        self.x_add = self.velocity
        self.y_add = 0
        self.eyes = Eyes()
        self.looking = (0, 0)
        self.WIN_PROXIMITY = 80
        self.WALL_TOLERANCE = 2

    def draw_self(self, x, y):
        """Draw Pinky to the screen"""
        noStroke()  # type: ignore
        fill(1.0, 0.5, 0.6)  # type: ignore
        ellipse(x, y, 100, 100)  # type: ignore
        bottom_half = createShape()  # type: ignore
        bottom_half.beginShape()
        bottom_half.vertex(x, y)
        bottom_half.vertex(x+100, y)
        bottom_half.vertex(x+100, y+50)
        bottom_half.vertex(x+50, y+25)
        bottom_half.vertex(x, y+50)
        bottom_half.endShape()
        shape(bottom_half, -50, 0)  # type: ignore

        self.eyes.display(x, y - 15, self.looking)

    def update(self):
        """Carry out necessary updates for each frame before
        drawing to screen"""
        # Check if Pinky is at an intersection
        on_vert = (
            (abs(self.x - self.maze.LEFT_VERT) < self.WALL_TOLERANCE) or
            (abs(self.x - self.maze.RIGHT_VERT) < self.WALL_TOLERANCE)
                   )
        on_horz = (
            (abs(self.y - self.maze.TOP_HORIZ) < self.WALL_TOLERANCE) or
            (abs(self.y - self.maze.BOTTOM_HORIZ) < self.WALL_TOLERANCE)
                   )

        # Check whether Pinky is up or down/left or right of Pacman
        up_down_part = self.pacman.y - self.y
        left_right_part = self.pacman.x - self.x

        # Update Pinky's eyes to look at Pacman
        self.update_eyes(up_down_part, left_right_part)

        # If Pinky gets close to Pacman, tell the GameController
        # that Pinky wins
        if (abs(up_down_part) < self.WIN_PROXIMITY and
                abs(left_right_part) < self.WIN_PROXIMITY):
            self.gc.pinky_wins = True

        # TODO:
        # PROBLEM 2: Make Pinky chase Pacman!
        # Study the code above and below these lines to understand how
        # Pinky's movements are calculated, and how Pinky's position with
        # respect to Pacman is represented.
        # Pinky should decide at each intersection whether to go left, right
        # up or down depending on which direction Pacman is further away in.
        # START CODE CHANGES
        
        # At an intersection choose the axis that brings Pinky closer to Pac-Man.
        if on_horz and on_vert:
            if abs(up_down_part) > abs(left_right_part):
                # Move vertically toward Pac-Man
                if up_down_part > 0:
                    self.x_add = 0
                    self.y_add = self.velocity
                else:
                    self.x_add = 0
                    self.y_add = -self.velocity
            else:
                # Move horizontally toward Pac-Man
                if left_right_part > 0:
                    self.x_add = self.velocity
                    self.y_add = 0
                else:
                    self.x_add = -self.velocity
                    self.y_add = 0
        # END CODE CHANGES

        # If the player wins, stop Pinky moving
        if self.gc.player_wins:
            self.x_add = 0
            self.y_add = 0

        # Move Pinky
        self.x = self.x + self.x_add
        self.y = self.y + self.y_add

    def update_eyes(self, up_down_part, left_right_part):
        """Set self.looking value based on position of Pinky w/r/t Pacman"""
        if up_down_part and abs(up_down_part) > 5:
            y = up_down_part/abs(up_down_part)
        else:
            y = 0
        if left_right_part and abs(left_right_part) > 5:
            x = left_right_part/abs(left_right_part)
        else:
            x = 0
        self.looking = (x, y)

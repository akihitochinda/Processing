from dots import Dots
# flake8: noqa

class Maze:
    """Draws the maze and handles interaction between Pacman and dots"""
    def __init__(self, WIDTH, HEIGHT,
                 LEFT_VERT, RIGHT_VERT,
                 TOP_HORIZ, BOTTOM_HORIZ,
                 game_controller):
        self.LEFT_VERT = LEFT_VERT
        self.RIGHT_VERT = RIGHT_VERT
        self.TOP_HORIZ = TOP_HORIZ
        self.BOTTOM_HORIZ = BOTTOM_HORIZ
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.gc = game_controller
        self.dots = Dots(WIDTH, HEIGHT,
                         LEFT_VERT, RIGHT_VERT,
                         TOP_HORIZ, BOTTOM_HORIZ)

    # TODO:
    # PROBLEM 3: implement dot eating
    # BEGIN CODE CHANGES
    def eat_dots(self, pacman):  # You might want/need to pass arguments here.
        self.dots.eat(pacman)
    # END CODE CHANGES

    def update(self):
        """Make necessary per-frame updates"""
        # Check whether the dots are all eaten
        if self.dots.dots_left() == 0:
            self.gc.player_wins = True

    def display(self):
        """Display the maze"""
        self.update()

        # Display the dots
        self.dots.display()

        # Draw the maze walls
        stroke(0.0, 0.0, 10)  # type: ignore
        strokeWeight(5)  # type: ignore
        fill(0)  # type: ignore
        rectMode(CORNER)  # type: ignore

        clearance = 60
        overdraw = 20  # Start drawing offscreen
        t = -(overdraw)
        l = -(overdraw)
        border = 20
        big_rad = 30
        small_rad = 17

        # Upper left
        t = -(overdraw)
        l = -(overdraw)
        w = self.LEFT_VERT - clearance + overdraw
        h = self.TOP_HORIZ - clearance + overdraw
        rect(l, t, w, h, big_rad)  # type: ignore
        rect(l, t, w - border, h - border, small_rad)  # type: ignore

        # Upper middle
        t = -(overdraw)
        l = self.LEFT_VERT + clearance
        w = (self.RIGHT_VERT - clearance) - (self.LEFT_VERT + clearance)
        rect(l, t, w, h, big_rad)  # type: ignore
        rect(l + border, t, w - border*2, h - border, small_rad)  # type: ignore

        # Upper right
        l = self.RIGHT_VERT + clearance
        w = self.RIGHT_VERT - clearance + overdraw
        rect(l, t, w, h, big_rad)  # type: ignore
        rect(l + border, t, w - border*2, h - border, small_rad)  # type: ignore

        # Middle left
        t = self.TOP_HORIZ + clearance
        l = -(overdraw)
        w = self.LEFT_VERT - clearance + overdraw
        h = (self.BOTTOM_HORIZ - clearance) - (self.TOP_HORIZ + clearance)
        rect(l, t, w, h, big_rad)  # type: ignore
        rect(l, t + border, w - border, h - border*2, small_rad)  # type: ignore

        # Middle middle
        l = self.LEFT_VERT + clearance
        t = self.TOP_HORIZ + clearance
        w = (self.RIGHT_VERT - clearance) - (self.LEFT_VERT + clearance)
        rect(l, t, w, h, big_rad)  # type: ignore
        rect(l + border, t + border, w - border*2, h - border*2,  # type: ignore
             small_rad)

        # Middle right
        l = self.RIGHT_VERT + clearance
        t = self.TOP_HORIZ + clearance
        w = self.RIGHT_VERT - clearance + overdraw
        rect(l, t, w, h, big_rad)  # type: ignore
        rect(l + border, t + border, w - border*2, h - border*2,  # type: ignore
             small_rad)

        # Lower left
        w = self.LEFT_VERT - clearance + overdraw
        h = self.TOP_HORIZ - clearance + overdraw
        l = -(overdraw)
        t = self.BOTTOM_HORIZ + clearance
        rect(l, t, w, h, big_rad)  # type: ignore
        rect(l, t + border, w - border, h - border, small_rad)  # type: ignore

        # Lower middle
        l = self.LEFT_VERT + clearance
        w = (self.RIGHT_VERT - clearance) - (self.LEFT_VERT + clearance)
        rect(l, t, w, h, big_rad)  # type: ignore
        rect(l + border, t + border, w - border*2, h - border,  # type: ignore
             small_rad)

        # Lower right
        l = self.RIGHT_VERT + clearance
        w = self.RIGHT_VERT - clearance + overdraw
        rect(l, t, w, h, big_rad)  # type: ignore
        rect(l + border, t + border, w - border*2, h - border,  # type: ignore
             small_rad)

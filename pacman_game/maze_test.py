from maze import Maze
from game_controller import GameController


def test_constructor():
    g = GameController(600, 400)
    m = Maze(600, 400, 150, 450,
             100, 300, g)
    assert m.LEFT_VERT == 150
    assert m.RIGHT_VERT == 450
    assert m.TOP_HORIZ == 100
    assert m.BOTTOM_HORIZ == 300
    assert m.WIDTH == 600
    assert m.HEIGHT == 400
    assert m.gc is g
    assert m.dots.dots_left() == ((m.dots.WIDTH//m.dots.SPACING + 1) * 2 +
                                  (m.dots.HEIGHT//m.dots.SPACING + 1) * 2)

# You'll see that two tests are failing when you run Pytest. They are related
# to the dot-eating functionality you wrote for Problem 3. Implement these
# tests so that they successfully test the dot-eating functionality.


def test_eat_dots():
    g = GameController(600, 400)
    m = Maze(600, 400, 150, 450,
             100, 300, g)

    class DummyPacman:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    # Eat a dot from the top row
    pacman = DummyPacman(m.dots.top_row[0].x, m.dots.top_row[0].y)
    m.eat_dots(pacman)
    assert len(m.dots.top_row) == (m.dots.WIDTH//m.dots.SPACING + 1) - 1

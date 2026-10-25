# flake8: noqa
class Dot:
    """A dot"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display(self):
        """Draws the dot"""
        fill(1, 0.5, 0.0)  # type: ignore
        ellipse(self.x, self.y, 10, 10)  # type: ignore

    def is_eaten(self, pacman):
        """Return True if Pacman is close enough to eat this dot.
        We look up the eat distance threshold from pacman's maze.dots if
        available, otherwise fall back to a sensible default.
        """
        try:
            threshold = pacman.maze.dots.EAT_DIST
        except Exception:
            threshold = 50
        dx = self.x - pacman.x
        dy = self.y - pacman.y
        return (dx*dx + dy*dy) ** 0.5 <= threshold

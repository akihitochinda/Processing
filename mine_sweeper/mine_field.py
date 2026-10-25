"""Lab 11 - Mine Sweeper"""
# For this exercise you'll complete the functionality of the Minesweeper game
# below, using a recursive method.

# What you need to do
# The expected behavior of the game is that when the player clicks on a cell
# that is revealed to be empty (no mine, and no number indicating adjacent
# mines) all adjacent empty and numbered cells are revealed. And furthermore,
# for any empty cell revealed in this way, all its adjacent empty and numbered
# cells are also revealed and so on (note the hints of recursion in that
# description of the behavior!) In this way, sometimes large swaths of clear
# space can be revealed in a single click.

# Your task is to implement this functionality using a single recursive method.
# Read the code and find the points in the code labeled :TODO. These are the
# only places that you need to make any changes. You should not define more
# than one new function, and the function must be recursive.

# Think about what this function needs to do. It will be called with a cell
# that has no neighboring mines. It needs to search through that cell's
# neighbors and determine which of those neighbors likewise need their
# neighbors searched through and uncovered. Numbered cells should be uncovered,
# but their neighbors should be left alone. Empty neighboring cells should be
# uncovered and their neighbors should also be handled in the same way as the
# current cell's neighbors (this is where the recursive aspect comes in).

from mine_field_cell import MineFieldCell


class MineField():

    def __init__(self, CELL_SIZE, FIELD_SIZE, numFont):
        self.CELL_SIZE = CELL_SIZE
        self.FIELD_SIZE = FIELD_SIZE
        self.cells = {}
        self.neighbors = [-1, 0, 1]
        for x in range(self.FIELD_SIZE):
            self.cells[x] = {}
            for y in range(self.FIELD_SIZE):
                self.cells[x][y] = MineFieldCell(
                                        x*self.CELL_SIZE,
                                        y*self.CELL_SIZE,
                                        self.CELL_SIZE,
                                        numFont
                                        )

    def reveal(self, x, y):
        """
        Reveal cells and carry out related action
        """
        self.cells[x][y].covered = False
        if self.cells[x][y].bomb:
            self.cells[x][y].explode = True
            self.gc.end_game('lose')
        else:
            self.check_completion_status()
        if self.cells[x][y].near_bombs == 0:
            # TODO: handle the case where an empty
            # cell is revealed. Use a recursive function
            # to do this
            self.reveal_neighbors(x, y)

    def reveal_neighbors(self, x, y):
        #  TODO: Define a recursive function to handle
        #  clearing out all empty/numbered neighbors of an empty
        #  cleared cell. Rewrite this dummy function with
        #  a suitable name and arguments.
        """
        Recursively reveal all empty/numbered neighbors
        of a given cell
        """
        for xneighbor in self.neighbors:
            for yneighbor in self.neighbors:
                # Skip the current cell and out-of-bounds neighbors
                if not ((xneighbor == 0 and yneighbor == 0)
                        or (x + xneighbor < 0)
                        or (y + yneighbor < 0)
                        or (x + xneighbor >= self.FIELD_SIZE)
                        or (y + yneighbor >= self.FIELD_SIZE)
                        ):
                    # Get neighbor cell
                    neighbor = self.cells[x+xneighbor][y+yneighbor]
                    # If neighbor is still covered up and not a bomb
                    if neighbor.covered and not neighbor.bomb:
                        # Reveal neighbor
                        neighbor.covered = False
                        # If neighbor is empty (0 bombs nearby),
                        # recursively reveal its neighbors
                        if neighbor.near_bombs == 0:
                            self.reveal_neighbors(x+xneighbor, y+yneighbor)

    def check_completion_status(self):
        """
        Check to see if all non-bomb cells have
        been uncovered
        """
        for x in range(self.FIELD_SIZE):
            for y in range(self.FIELD_SIZE):
                if (self.cells[x][y].covered and
                   not self.cells[x][y].bomb):
                    return
        self.gc.end_game('win')

    def neighbor_bomb_count(self, x, y):
        """
        Get the count of adjacentn bombs for
        a cell
        """
        neighbor_bombs = 0
        for xneighbor in self.neighbors:
            for yneighbor in self.neighbors:
                if not ((xneighbor == 0 and yneighbor == 0)
                        or (x + xneighbor < 0)
                        or (y + yneighbor < 0)
                        or (x + xneighbor >= self.FIELD_SIZE)
                        or (y + yneighbor >= self.FIELD_SIZE)
                        ):
                    if self.cells[x+xneighbor][y+yneighbor].bomb:
                        neighbor_bombs += 1
        return neighbor_bombs

    def loop_through_field(self, fn):
        """
        loops through mine field and carries
        out passed function with x and y arguments
        """
        # This will save some reduplication of code in the
        # following methods
        for x in range(self.FIELD_SIZE):
            for y in range(self.FIELD_SIZE):
                fn(x, y)

    def update(self):
        """
        Update all cells
        """
        self.loop_through_field(
            lambda x, y: self.cells[x][y].update()
            )

    def reveal_all(self):
        """
        Reveal all cells
        """
        self.loop_through_field(
            lambda x, y: self.cells[x][y].reveal()
            )

    def plant_mines(self, mines):
        """
        Add mines to appropriate cells
        """
        for mine in mines:
            self.cells[mine[0]][mine[1]].bomb = True
        self.loop_through_field(
                self.set_count
            )

    def set_count(self, x, y):
        """
        Sets the neighboring bomb count for a position
        """
        if not self.cells[x][y].bomb:
            self.cells[x][y].near_bombs =\
                self.neighbor_bomb_count(x, y)

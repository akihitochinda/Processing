# flake8: noqa
import random

"""Project: Gomoku (Continued)"""
# The Assignment, Part 2: Full Gomoku game:
# For the second part of the assignment you'll complete the implementation of
# the full Gomoku game, complete with an Connect Four-playing AI.

# For the first part of the assignment, you'll turn in the following:
# - The full Gomoku game
#    - Play on a board of 15 rows and 15 columns
#    - Pit a computer player against a human
#    - Recognize a five-in-a-row sequence and end the game
#    - Announce the winner
#    - Save the winner's name to a file
#    - Keep track of the number of wins for each player in this file
# - Tell us about your computer player
# - Write a test suite using Pytest

"""1. Code For Part 2"""
# Your final Gomooku game will do the following:
#  - Play on an 15x15 board
#  - Use at least one module (external class) to move as much functionality
#    out of the main Processing sketch file as possible.
#  - Begin, similarly to the Part 1 version, with stones placed on the board,
#    alternating black and white
#  - Let the user go first, playing the black stone
#     - If there are no more legal moves, end the game.
#  - The computer goes next, after a brief pause, choosing the "best" square,
#    determined by the AI part of your code, described below.
#     - The computer always places a stone in an open position, unless the
#       game is over.
#     - Use a countdown value to create a delay, so the computer's move isn't
#       unnaturally instantaneous.
#     - If there are no more legal moves, end the game.
#  - Alternate back and forth between user moves and AI moves.
#  - When one player has five in sequence horizontally, vertically, or
#    diagonally, or the board is full, announce that the game is over, and the
#    winner if there is one.
#     - Prompt the user for their name and save it in the scores file (see
#       details below).
# The human player always plays black stones and goes first, and the computer
# player always white stones. It's OK if your computer player takes some time
# to pick their move, depending on how elaborate your AI gets, but the
# computer's response should not be instantaneous, and shouldn't take more
# than a few seconds (about 5 seconds should be a reasonable max).

"""2. Scores file"""
# At the end of game play, no matter how it ended, prompt the user for their
# name and save their name and score in a file. The file is named scores.txt.
# The format is one score per line with a space between the user's name and
# their score. You've done a fair amount of reading from files, so file
# handling isn't new to you.

# User scores represent the number of games the user has won. The highest user
# score is always the first entry in the file. If a game ends in a draw, treat
# this as two losses and do not update the scores file. Otherwise find the
# name of the winner in the file and increment their score (or add them to the
# file if they're not there yet).

# For example, let's say that the following four players have all played the
# game multiple times. Emilia won 5 times, Iago won 2 times, Desdemona won 2
# times, and Cassio won 1 time. The scores file would contain:
# Emilia 5
# Iago 2
# Desdemona 2
# Cassio 1
# You can assume that, when you prompt the user for their name, they enter a
# string. It might have spaces in it, though. Assume that user names are
# unique, so if a matching user name to the current winner is in the file, you
# will increment that user's score by 1. The scores file should always remain
# ranked from highest score to lowest score.

# Note: the Processing Python environment isn't running from a real terminal.
# In fact, all of Processing runs on top of a layer of Java. For this reason,
# we can't use the native Python input function. No fear, however, we can get
# an interactive text input by defining the following input function of our
# own, (with just a smidgen of Java). The definition of input is shown below,
# inside a brief demo sketch that includes only a setup() function that uses
# it. Try out this code and use the input function verbatim in your project:

# def setup():
#     answer = input('enter your name')
#     if answer:
#         print('hi ' + answer)
#     elif answer == '':
#         print('[empty string]')
#     else:
#         print(answer) # Canceled dialog will print None

# def input(self, message=''):
#     from javax.swing import JOptionPane
#     return JOptionPane.showInputDialog(frame, message)

"""3. Computer vs. Human"""
# - Filename: ai.txt
# Your solution will allow the computer to play against a human adversary. The
# most basic requirement is that the computer always makes a legal move if
# there is one to make.
# Then, you can earn extra credit points by making your AI scheme effective
# and a really good Gomoku player. Either way, you need to tell us how you
# approached it. In your ai.txt file, answer these questions:
# - Did you attempt to make your computer player very smart -- i.e., do
#   something more clever than just pick a random legal move?
# - If so, were you able to accomplish this? Is your computer player as smart
#   as you would like?
# - How did you determine which piece to play next? Tell us about your "pick
#   next move" algorithm
# - How often did your computer program beat you, or your friends, or whoever
#   tested it out for you?
# - How easy would it be to make the difficulty level adjustable?
# - How would you improve it in the future?

"""4. Testing suite"""
# Include a test file for each module you write, testing all non-graphical
# functionality. In your test suite, you must:
#  - Test every function, except those concerned only with graphics (i.e.
#    those which make calls to Processing functions). Use separate test files
#    for separate modules, and name the files accordingly.
#  - Write one test for every function you're testing, named something like
#    test_func1, test_func2, etc. Each of these test functions should validate
#    possible inputs against expected outputs.
#  - For example, a function or method named init_board that takes in the size
#    of the board and returns a nested list should be tested with various
#    inputs, including:
#     - Board of size 0 returns []
#     - Board of size nxn returns a list of n lists, each of n positions.

# Helpful hints:
# You'll need to switch back-and-forth between the user's turn and the
# computer's turn. Here's how I did that (of course, your approach can be
# totally different -- consider this information if it's helpful). I handled
# mousePressed value is true in the top level Processing sketch, where it has
# access to mouseX and mouseY. The computer_make_move() is executed in draw()
# inside an if conditional structure that checks to make sure that it is the
# computer's turn and that the time delay counter for the pause has run down
# to zero.


class Game:
    """Class representing a Gomoku game."""
    def __init__(self, board_size, width, height):
        """Initialize the Gomoku game."""
        self.board_size = board_size
        self.width = width
        self.height = height
        self.margin = 36000 // (height + width)
        self.cell_size = float(width - 2 * self.margin) / (board_size - 1)
        self.stone_radius = self.cell_size / 2.2

        # Game state
        self.board = [
            [None for _ in range(board_size)]
            for _ in range(board_size)
        ]
        self.current_player = "black"  # "black" or "white"
        self.game_over = False
        self.winner = None
        self.move_count = 0

    def draw_board(self):
        """Draw the game board."""
        stroke(0)  # type: ignore
        strokeWeight(4)  # type: ignore

        # Draw grid lines
        for i in range(self.board_size):
            x = self.margin + i * self.cell_size
            y = self.margin + i * self.cell_size

            # Vertical lines
            line(x, self.margin, x, self.height - self.margin)  # type: ignore
            # Horizontal lines
            line(self.margin, y, self.width - self.margin, y)  # type: ignore

    def draw_stones(self):
        """Draw all stones on the board."""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] is not None:
                    x = self.margin + col * self.cell_size
                    y = self.margin + row * self.cell_size

                    if self.board[row][col] == "black":
                        noStroke()  # type: ignore
                        fill(0)  # type: ignore
                    else:
                        stroke(0)  # type: ignore
                        strokeWeight(2)  # type: ignore
                        fill(1)  # type: ignore

                    ellipse(x, y, self.stone_radius * 2,  # type: ignore
                            self.stone_radius * 2)

    def handle_click(self, mouse_x, mouse_y):
        """Handle mouse click to place a stone."""
        if self.game_over:
            return

        # Convert pixel coordinates to grid coordinates
        grid_col = int(round((mouse_x - self.margin) / float(self.cell_size)))
        grid_row = int(round((mouse_y - self.margin) / float(self.cell_size)))

        # Check if click is within valid board range
        if not (0 <= grid_row < self.board_size and
                0 <= grid_col < self.board_size):
            return

        # Check if position is empty
        if self.board[grid_row][grid_col] is not None:
            return

        # Place stone
        self.board[grid_row][grid_col] = self.current_player
        self.move_count += 1

        # Check for winner
        if self.check_winner(grid_row, grid_col):
            self.game_over = True
            self.winner = self.current_player
            return

        # Check for draw (board full)
        if self.move_count >= self.board_size * self.board_size:
            self.game_over = True
            return

        # Switch players
        if self.current_player == "black":
            self.current_player = "white"
        else:
            self.current_player = "black"

    def get_random_move(self):
        """Get a smart move for AI (with fallback to random).
        Open-ended threats are prioritized for offensive moves."""
        opponent = "white" if self.current_player == "black" else "black"

        # 1. Win/Block immediate win (5 in a row)
        offensive_move_five = self.find_threat_move(self.current_player, 5)
        if offensive_move_five:
            return offensive_move_five
    
        block_move_five = self.find_threat_move(opponent, 5)
        if block_move_five:
            return block_move_five

        # 2. Create offensive/defensive threat
        offensive_move_four = self.find_threat_move(
            self.current_player, 4, require_open=True
        )
        if offensive_move_four:
            return offensive_move_four

        block_move_four = self.find_threat_move(opponent, 4)
        if block_move_four:
            return block_move_four

        offensive_move_three = self.find_threat_move(
            self.current_player, 3, require_open=True
        )
        if offensive_move_three:
            return offensive_move_three

        block_move_three = self.find_threat_move(opponent, 3)
        if block_move_three:
            return block_move_three

        offensive_move_two = self.find_threat_move(
            self.current_player, 2, require_open=True
        )
        if offensive_move_two:
            return offensive_move_two

        # 3. Otherwise pick strategic move near existing stones
        # Find positions near existing stones (within 2 cell)
        strategic_positions = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] is None:
                    # Check if near any existing stone
                    if self.is_near_stone(row, col, 2):
                        strategic_positions.append((row, col))

        # If strategic positions exist, choose randomly from them
        if strategic_positions:
            return random.choice(strategic_positions)
        return None

    def find_threat_move(self, player, count, require_open=False):
        """Find a move that creates consecutive stones (prefer open-ended)."""
        open_threats = []
        closed_threats = []

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] is None:
                    # Try placing this stone
                    self.board[row][col] = player
                    has_threat, is_open, has_space = self.check_consecutive(
                        row, col, count
                    )
                    self.board[row][col] = None  # Undo

                    # For offensive moves, reject if no space to reach 5
                    # For defensive moves, ignore space requirement
                    if has_threat and (not require_open or has_space):
                        if is_open:
                            open_threats.append((row, col))
                        else:
                            closed_threats.append((row, col))

        # Prefer open threats over closed ones
        if open_threats:
            return open_threats[0]  # Always prefer open
        elif closed_threats and not require_open:  # Only for defensive moves
            return closed_threats[0]
        return None  # Offense with no open threats returns None

    def is_near_stone(self, row, col, distance):
        """Check if position (row, col) is within distance of any stone."""
        for r in range(max(0, row - distance),
                       min(self.board_size, row + distance + 1)):
            for c in range(max(0, col - distance),
                           min(self.board_size, col + distance + 1)):
                if self.board[r][c] is not None:
                    return True
        return False

    def check_consecutive(self, row, col, min_count):
        """Check if position (row, col) creates consecutive stones.
        Returns tuple: (has_count, is_open, has_space_for_five) where:
        - has_count means at least min_count stones in a row
        - is_open means at least one end is open
        - has_space_for_five means total space (stones + empty) >= 5"""
        directions = [
            (1, 0),   # Horizontal
            (0, 1),   # Vertical
            (1, 1),   # Diagonal down-right
            (1, -1)   # Diagonal up-right
        ]
        current_color = self.board[row][col]

        has_count = False
        is_open = False
        has_space_for_five = False

        for dr, dc in directions:
            count = 1

            # Check in the positive direction
            r, c = row + dr, col + dc
            while (0 <= r < self.board_size and
                   0 <= c < self.board_size and
                   self.board[r][c] == current_color):
                count += 1
                r += dr
                c += dc
            end_pos = (r, c)

            # Check in the negative direction
            r, c = row - dr, col - dc
            while (0 <= r < self.board_size and
                   0 <= c < self.board_size and
                   self.board[r][c] == current_color):
                count += 1
                r -= dr
                c -= dc
            start_pos = (r, c)

            if count >= min_count:
                has_count = True

                # Check if either end is open (empty and in bounds)
                pos_open = (0 <= end_pos[0] < self.board_size and
                            0 <= end_pos[1] < self.board_size and
                            self.board[end_pos[0]][end_pos[1]] is None)

                neg_open = (0 <= start_pos[0] < self.board_size and
                            0 <= start_pos[1] < self.board_size and
                            self.board[start_pos[0]][start_pos[1]] is None)

                if pos_open or neg_open:
                    is_open = True

                # Check total space (stones + empty spaces on both ends)
                total_space = count

                # Count empty spaces after end
                r, c = end_pos[0], end_pos[1]
                while (0 <= r < self.board_size and
                       0 <= c < self.board_size and
                       self.board[r][c] is None):
                    total_space += 1
                    r += dr
                    c += dc

                # Count empty spaces before start
                r, c = start_pos[0], start_pos[1]
                while (0 <= r < self.board_size and
                       0 <= c < self.board_size and
                       self.board[r][c] is None):
                    total_space += 1
                    r -= dr
                    c -= dc

                if total_space >= 5:
                    has_space_for_five = True

        return (has_count, is_open, has_space_for_five)

    def place_ai_move(self, row, col):
        """Place AI stone at specified position."""
        if self.board[row][col] is None and not self.game_over:
            self.board[row][col] = self.current_player
            self.move_count += 1

            if self.check_winner(row, col):
                self.game_over = True
                self.winner = self.current_player
            elif self.move_count >= self.board_size * self.board_size:
                self.game_over = True
            else:
                # Switch players
                if self.current_player == "black":
                    self.current_player = "white"
                else:
                    self.current_player = "black"
            return True

        return False

    def check_winner(self, row, col):
        """Check if the last move at (row, col) creates a winning condition."""
        has_five, _, _ = self.check_consecutive(row, col, 5)
        return has_five

    def display_winner(self):
        """Display winner message on screen."""
        if self.game_over:
            fill(0.6, 0.9, 0.6)  # type: ignore
            textSize((self.width + self.height) // 15)  # type: ignore
            textAlign(CENTER, TOP)  # type: ignore

            if self.winner:
                text("{} wins!".format(self.winner),   # type: ignore
                     self.width // 2, self.height / 1.4)
            else:
                text("game over - draw!",  # type: ignore
                     self.width // 2, self.height / 1.4)

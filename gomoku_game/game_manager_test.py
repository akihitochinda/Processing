import os
from gomoku import Game
from game_manager import GameManager


def test_init():
    # Test GameManager initialization
    game = Game(15, 600, 600)
    gm = GameManager(game, "TestPlayer")
    assert gm.game == game
    assert gm.player_name == "TestPlayer"
    assert gm.is_player_turn is True
    assert gm.delay_counter == 0
    assert gm.delay_frames == 60
    assert gm.game_ended is False


def test_player_make_move():
    # Test player's move handling
    game = Game(15, 600, 600)
    gm = GameManager(game, "TestPlayer")

    # Calculate valid click position for (0, 0)
    click_x = game.margin
    click_y = game.margin

    # Test valid move
    assert gm.player_make_move(click_x, click_y) is True
    assert gm.is_player_turn is False
    assert gm.delay_counter == 60

    # Test game over condition
    game.game_over = True
    assert gm.player_make_move(click_x, click_y) is False

    # Test invalid move (click outside board)
    old_turn = gm.is_player_turn
    assert gm.player_make_move(-100, -100) is False
    assert gm.is_player_turn == old_turn


def test_computer_make_move():
    # Test computer's move handling with delay
    game = Game(15, 600, 600)
    gm = GameManager(game, "TestPlayer")
    gm.is_player_turn = False
    gm.delay_counter = 10

    # Test delay countdown
    assert gm.computer_make_move() is False  # Still delaying
    assert gm.delay_counter == 9

    # Place a stone so computer has nearby position
    game.board[7][7] = "black"

    # Test computer move after delay
    gm.is_player_turn = False
    gm.delay_counter = 0

    assert gm.computer_make_move() is True
    assert gm.is_player_turn is True

    # Test game over condition
    game.game_over = True
    gm.is_player_turn = False
    gm.delay_counter = 0

    assert gm.computer_make_move() is False


def test_save_score():
    game = Game(15, 600, 600)
    gm = GameManager(game, "NewPlayer")

    # Clean up test file if exists
    if os.path.exists("scores.txt"):
        os.remove("scores.txt")

    # Test adding new player
    game.winner = 'white'
    gm.save_score("NewPlayer")

    with open("scores.txt", 'r') as f:
        content = f.read().strip()
        assert content == "NewPlayer 0"

    # Test updating existing player's score
    game.winner = 'black'
    gm = GameManager(game, "Player")

    # Clean up test file if exists
    if os.path.exists("scores.txt"):
        os.remove("scores.txt")
    # Create initial score
    with open("scores.txt", 'w') as f:
        f.write("Player 3\n")
    gm.save_score("Player")

    with open("scores.txt", 'r') as f:
        content = f.read().strip()
        assert content == "Player 4"

    # Test multiple players and sorting
    gm = GameManager(game, "PlayerC")

    # Clean up test file if exists
    if os.path.exists("scores.txt"):
        os.remove("scores.txt")
    # Create initial scores
    with open("scores.txt", 'w') as f:
        f.write("PlayerA 5\n")
        f.write("PlayerB 2\n")
        f.write("PlayerC 2\n")
    gm.save_score("PlayerC")

    with open("scores.txt", 'r') as f:
        lines = f.readlines()
        assert lines[0].strip() == "PlayerA 5"
        assert lines[1].strip() == "PlayerC 3"
        assert lines[2].strip() == "PlayerB 2"

    gm = GameManager(game, "Player")

    # Clean up test file if exists
    if os.path.exists("scores.txt"):
        os.remove("scores.txt")

    # Add multiple scores
    gm.save_score("Alice")
    gm.save_score("Bob")
    gm.save_score("Alice")
    gm.save_score("Charlie")

    with open("scores.txt", 'r') as f:
        lines = f.readlines()
        assert "Alice 2" in lines[0]
        assert "Bob 1" in lines[1] or "Charlie 1" in lines[1]
    # Cleanup
    os.remove("scores.txt")

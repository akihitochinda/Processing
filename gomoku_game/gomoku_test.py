from gomoku import Game


def test_init_board():
    # Test board initialization for size 0 returns empty list
    game = Game(0, 600, 600)
    assert game.board_size == 0
    assert game.board == []

    # Test board of size nxn returns list of n lists, each of n positions
    game = Game(15, 600, 600)
    assert game.board_size == 15
    assert len(game.board) == 15
    assert len(game.board[0]) == 15
    assert all(len(row) == 15 for row in game.board)
    assert all(game.board[i][j] is None
               for i in range(15) for j in range(15))

    # Test other attributes
    assert game.current_player == "black"
    assert game.game_over is False
    assert game.winner is None
    assert game.move_count == 0
    assert game.margin == 36000 // 1200
    assert isinstance(game.cell_size, float)


def test_place_ai_move():
    # Test placing AI moves and game state updates
    game = Game(15, 600, 600)
    assert game.place_ai_move(0, 0) is True
    assert game.board[0][0] == "black"
    assert game.move_count == 1
    assert game.place_ai_move(0, 0) is False

    # Test turn switching and win detection
    assert game.current_player == "white"

    for col in range(4):
        game.board[0][col] = "white"
    game.place_ai_move(0, 4)
    assert game.game_over is True
    assert game.winner == "white"

    # Test draw condition
    game = Game(3, 600, 600)
    game.board[0] = ["black", "white", "black"]
    game.board[1] = ["white", "black", "white"]
    game.board[2] = ["white", "black", None]
    game.move_count = 8
    game.place_ai_move(2, 2)
    assert game.game_over is True
    assert game.winner is None


def test_check_winner():
    # Test winner detection in different directions
    game = Game(15, 600, 600)
    for col in range(5):
        game.board[0][col] = "black"
    assert game.check_winner(0, 2) is True

    game = Game(15, 600, 600)
    for row in range(5):
        game.board[row][0] = "black"
    assert game.check_winner(2, 0) is True

    game = Game(15, 600, 600)
    for i in range(5):
        game.board[i][i] = "black"
    assert game.check_winner(2, 2) is True

    game = Game(15, 600, 600)
    for col in range(4):
        game.board[0][col] = "black"
    assert game.check_winner(0, 1) is False


def test_is_near_stone():
    # Test proximity detection for stones on the board
    game = Game(15, 600, 600)
    game.board[5][5] = "black"
    assert game.is_near_stone(6, 6, 2) is True
    assert game.is_near_stone(10, 10, 2) is False


def test_check_consecutive():
    # Test consecutive stones detection and open ends
    game = Game(15, 600, 600)
    game.board[0][1] = "black"
    game.board[0][2] = "black"
    game.board[0][3] = "black"
    has_count, is_open, has_space = game.check_consecutive(0, 2, 3)
    assert has_count is True
    assert is_open is True
    assert has_space is True

    game.board[0][0] = "white"
    game.board[0][1] = "black"
    game.board[0][2] = "black"
    game.board[0][3] = "black"
    game.board[0][4] = "white"
    has_count, is_open, has_space = game.check_consecutive(0, 2, 3)
    assert has_count is True
    assert is_open is False
    assert has_space is False


def test_find_threat_move():
    # Test finding threat moves for a given player and count
    game = Game(15, 600, 600)
    for col in range(4):
        game.board[0][col] = "white"
    move = game.find_threat_move("white", 5, require_open=False)
    assert move == (0, 4)
    assert move is not None  # Should find a move

    game.board[0][0] = "white"
    game.board[0][1] = "white"
    game.board[0][3] = "black"
    move = game.find_threat_move("white", 3, require_open=True)
    # Should not choose (0,2) if it creates dead pattern
    if move == (0, 2):
        game.board[0][2] = "white"
        _, _, has_space = game.check_consecutive(0, 2, 3)
        game.board[0][2] = None
        assert has_space is True  # Only accept if has space


def test_get_random_move():
    # Test AI move selection prioritizing threats
    game = Game(15, 600, 600)
    game.current_player = "white"
    for col in range(4):
        game.board[0][col] = "white"
    move = game.get_random_move()
    assert move == (0, 4)

    for col in range(4):
        game.board[0][col] = "black"
    move = game.get_random_move()
    assert move == (0, 4)

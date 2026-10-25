import os


class GameManager:
    """Maintains the state of the game."""
    def __init__(self, game, player_name):
        self.game = game
        self.player_name = player_name
        self.is_player_turn = True
        self.delay_counter = 0
        self.delay_frames = 60  # Delay for 1 second at 60 FPS
        self.game_ended = False

    def player_make_move(self, mouse_x, mouse_y):
        """Handle player's move."""
        if not self.is_player_turn or self.game.game_over:
            return False

        old_move_count = self.game.move_count
        self.game.handle_click(mouse_x, mouse_y)

        # Check if a move was made
        if self.game.move_count > old_move_count:
            self.is_player_turn = False
            self.delay_counter = self.delay_frames
            return True
        return False

    def computer_make_move(self):
        """Handle computer's move with delay."""
        if self.is_player_turn or self.game.game_over:
            return False

        # Countdown delay
        if self.delay_counter > 0:
            # Waiting for delay to finish before computer moves
            self.delay_counter -= 1
            return False

        # Make computer move
        move = self.game.get_random_move()
        if move:
            row, col = move
            self.game.place_ai_move(row, col)
            self.is_player_turn = True
            return True
        return False

    def save_score(self, name):
        """Save the winner's score to scores.txt."""
        scores = {}
        filepath = "scores.txt"

        # Read existing scores
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    for line in f:
                        parts = line.strip().split(' ', 1)
                        if len(parts) == 2:
                            player_name = parts[0]
                            score = int(parts[1])
                            scores[player_name] = score
            except Exception as e:
                print("Error reading scores file:", e)

        # Update winner's score
        if self.game.winner == 'black':
            if name in scores:
                scores[name] += 1
            else:
                scores[name] = 1
        else:
            if name not in scores:
                scores[name] = 0

        # Sort by score (descending)
        sorted_scores = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Write back to file
        with open(filepath, 'w') as f:
            for player_name, score in sorted_scores:
                f.write("{} {}\n".format(player_name, score))

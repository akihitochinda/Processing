from gomoku import Game
from game_manager import GameManager

HEIGHT = 600
WIDTH = 600
BOARD_SIZE = 15

game = Game(BOARD_SIZE, WIDTH, HEIGHT)
game_manager = None
player_name = ""
name_asked = False  # Flag to avoid prompts every single frame

def setup():
    global game_manager
    size(WIDTH, HEIGHT)
    colorMode(RGB, 1)
    game_manager = GameManager(game, player_name)

#    answer = input('enter your name')
#    if answer:
#        print('hi ' + answer)
#    elif answer == '':
#        print('[empty string]')
#    else:
#        print(answer) # Canceled dialog will print None

# Java module error with JOptionPane
# def input(self, message=''):
#     from javax.swing import JOptionPane
#     return JOptionPane.showInputDialog(frame, message)

def draw():
    global player_name, name_asked
    background(0.8, 0.6, 0.4)
    game.draw_board()
    game.draw_stones()
    game.display_winner()

    # Handle computer move
    game_manager.computer_make_move()

    # Name input prompt
    if game.game_over and not name_asked and game_manager.player_name == "":
        name_asked = True
        println("enter your name")
    
    if name_asked:
        # Draw semi-transparent overlay
        fill(0, 0, 0, 0.7)
        rect(0, 0, WIDTH, HEIGHT)
        
        # Draw styled popup box
        fill(0.95, 0.95, 0.95)
        stroke(0.3, 0.3, 0.3)
        strokeWeight(3)
        rectMode(CENTER)
        rect(WIDTH / 2, HEIGHT / 2, 400, 200, 20)  # Rounded corners
        
        # Draw title
        fill(0.2, 0.4, 0.7)
        textSize(32)
        textAlign(CENTER, CENTER)
        text("Game Over!", WIDTH / 2, HEIGHT / 2 - 60)
        
        # Draw input label
        fill(0.1, 0.1, 0.1)
        textSize(20)
        text("Enter your name:", WIDTH / 2, HEIGHT / 2 - 20)
        
        # Draw input box
        fill(1, 1, 1)
        stroke(0.4, 0.4, 0.4)
        strokeWeight(2)
        rectMode(CENTER)
        rect(WIDTH / 2, HEIGHT / 2 + 20, 300, 40, 5)
        
        # Draw typed text with cursor
        fill(0, 0, 0)
        textSize(22)
        text(player_name + "_", WIDTH / 2, HEIGHT / 2 + 20)
        
        # Draw instruction
        fill(0.3, 0.3, 0.3)
        textSize(16)
        text("Press ENTER to confirm", WIDTH / 2, HEIGHT / 2 + 70)
        
        strokeWeight(1)
        rectMode(CORNER)
        return

def mousePressed():
    """Handle mouse press to place stones"""
    # game.handle_click(mouseX, mouseY)
    game_manager.player_make_move(mouseX, mouseY)

def keyPressed():
    """Handle keyboard input for name entry"""
    global player_name, name_asked
    
    if name_asked:
        if key == '\n' or key == '\r':  # ENTER
            if player_name.strip():
                game_manager.player_name = player_name.strip()
                println('hi ' + player_name)
            elif player_name == "":
                game_manager.player_name = "Anonymous"
                println('[empty string]')
            else:
                println(player_name)  # Canceled dialog will print None
            game_manager.save_score(game_manager.player_name)
            name_asked = False
        elif key == '\b':  # BACKSPACE
            if len(player_name) > 0:
                player_name = player_name[:-1]
        elif key != CODED and len(player_name) < 20:
            player_name += key

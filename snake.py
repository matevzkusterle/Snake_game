import curses
import random

# Setup the window
def setup_window():
    window = curses.initscr()
    curses.curs_set(0)
    sh, sw = window.getmaxyx()
    window.keypad(True)
    window.timeout(100)  # Controls the speed of the snake
    return window, sh, sw

# Snake and food initial position setup
def initialize_game(sh, sw):
    snake_x = sw // 4
    snake_y = sh // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    food = [sh // 2, sw // 2]
    window.addch(food[0], food[1], curses.ACS_PI)
    return snake, food

# Check if the snake collides with itself or the window borders
def check_collision(snake, sh, sw):
    if (snake[0][0] in [0, sh]) or (snake[0][1] in [0, sw]) or (snake[0] in snake[1:]):
        return True
    return False

# Main game loop
def main(window):
    sh, sw = window.getmaxyx()
    snake, food = initialize_game(sh, sw)
    key = curses.KEY_RIGHT
    score = 0
    
    while True:
        next_key = window.getch()
        key = key if next_key == -1 else next_key
        
        # Calculate new position of the snake's head
        if key == curses.KEY_RIGHT:
            new_head = [snake[0][0], snake[0][1] + 1]
        elif key == curses.KEY_LEFT:
            new_head = [snake[0][0], snake[0][1] - 1]
        elif key == curses.KEY_UP:
            new_head = [snake[0][0] - 1, snake[0][1]]
        elif key == curses.KEY_DOWN:
            new_head = [snake[0][0] + 1, snake[0][1]]
        else:
            continue

        snake.insert(0, new_head)
        
        # Check if snake hits the wall or itself
        if check_collision(snake, sh, sw):
            curses.endwin()
            print(f"Game Over! Your Score: {score}")
            quit()

        # Check if snake eats the food
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                nf = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
                food = nf if nf not in snake else None
            window.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            window.addch(tail[0], tail[1], ' ')

        # Update the snake's position
        window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

if __name__ == "__main__":
    window, sh, sw = setup_window()
    try:
        main(window)
    finally:
        curses.endwin()


#you need to install windows-curses with pip3
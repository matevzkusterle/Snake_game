import curses
import random

# Setup the window
def setup_window():
    window = curses.initscr()  # Initialize the curses screen and return a window object.
    curses.curs_set(0)  # Make the cursor invisible for a better game experience.
    sh, sw = window.getmaxyx()  # Get the dimensions of the terminal window (rows and columns).
    window.keypad(True)  # Enable keypad input to capture arrow keys.
    window.timeout(100)  # Set a timeout for `getch()` to control the snake's speed (100ms).
    return window, sh, sw  # Return the window object and its dimensions.

# Snake and food initial position setup
def initialize_game(sh, sw):
    snake_x = sw // 4  # Set the initial x-coordinate of the snake's head to 1/4th of the screen width.
    snake_y = sh // 2  # Set the initial y-coordinate of the snake's head to the middle of the screen height.
    snake = [  # Define the initial snake as a list of coordinates (head and two body parts).
        [snake_y, snake_x],  # Head of the snake.
        [snake_y, snake_x - 1],  # First body segment (left of the head).
        [snake_y, snake_x - 2]  # Second body segment (left of the first segment).
    ]
    food = [sh // 2, sw // 2]  # Place the initial food at the center of the screen.
    window.addch(food[0], food[1], curses.ACS_PI)  # Display the food on the screen using a special character (π).
    return snake, food  # Return the snake's initial position and the food's position.

# Check if the snake collides with itself or the window borders
def check_collision(snake, sh, sw):
    if (snake[0][0] in [0, sh]) or (snake[0][1] in [0, sw]):  
        # Check if the snake's head hits the top/bottom or left/right borders of the screen.
        return True
    if snake[0] in snake[1:]:  
        # Check if the snake's head collides with its own body.
        return True
    return False  # If no collision is detected, return False.

# Main game loop
def main(window):
    sh, sw = window.getmaxyx()  # Get the dimensions of the terminal window.
    snake, food = initialize_game(sh, sw)  # Initialize the snake and food positions.
    key = curses.KEY_RIGHT  # Set the initial direction of the snake to move right.
    score = 0  # Initialize the player's score to 0.
    
    while True:  # Start the main game loop.
        next_key = window.getch()  # Get the next key pressed by the user.
        key = key if next_key == -1 else next_key  
        # If no key is pressed, continue moving in the current direction; otherwise, update the direction.

        # Calculate the new position of the snake's head based on the direction.
        if key == curses.KEY_RIGHT:
            new_head = [snake[0][0], snake[0][1] + 1]  # Move right (increase x-coordinate).
        elif key == curses.KEY_LEFT:
            new_head = [snake[0][0], snake[0][1] - 1]  # Move left (decrease x-coordinate).
        elif key == curses.KEY_UP:
            new_head = [snake[0][0] - 1, snake[0][1]]  # Move up (decrease y-coordinate).
        elif key == curses.KEY_DOWN:
            new_head = [snake[0][0] + 1, snake[0][1]]  # Move down (increase y-coordinate).
        else:
            continue  # Ignore invalid keys and continue the loop.

        snake.insert(0, new_head)  # Add the new head position to the front of the snake.

        # Check if the snake collides with the wall or itself.
        if check_collision(snake, sh, sw):
            curses.endwin()  # End the curses window mode.
            print(f"Game Over! Your Score: {score}")  # Print the final score.
            quit()  # Exit the program.

        # Check if the snake eats the food.
        if snake[0] == food:
            score += 1  # Increase the score by 1.
            food = None  # Remove the current food.
            while food is None:  # Generate a new food position.
                nf = [random.randint(1, sh - 2), random.randint(1, sw - 2)]  
                # Randomly place the food within the screen boundaries.
                food = nf if nf not in snake else None  
                # Ensure the new food position does not overlap with the snake.
            window.addch(food[0], food[1], curses.ACS_PI)  # Display the new food on the screen.
        else:
            tail = snake.pop()  # Remove the last segment of the snake (to simulate movement).
            window.addch(tail[0], tail[1], ' ')  # Clear the tail's position on the screen.

        # Update the snake's position on the screen.
        window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)  
        # Display the snake's head using a special character.

if __name__ == "__main__":
    window, sh, sw = setup_window()  # Initialize the game window and get its dimensions.
    try:
        main(window)  # Start the main game loop.
    finally:
        curses.endwin()  # Ensure the curses window mode is properly terminated, even if an error occurs.

#you need to install windows-curses with pip3
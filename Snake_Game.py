from tkinter import *
from tkinter import messagebox
from tkinter import Button
import random
import time

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100  # Increased the speed for demonstration purposes
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, GAME_WIDTH / SPACE_SIZE - 1) * SPACE_SIZE
        y = random.randint(0, GAME_HEIGHT / SPACE_SIZE - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag='food')


def next_turn(snake, food):
    global direction, score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Check if the snake's head touches the boundaries
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        game_over()  # Call the game_over() function if boundaries are reached
        return

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        # Snake has eaten the food
        score += 1
        label.config(text="Score:{}".format(score))

        # Remove the eaten food
        canvas.delete('food')

        # Create new food
        food = Food()

    else:
        # Remove the tail of the snake
        canvas.delete(snake.squares[-1])
        snake.squares.pop()
        snake.coordinates.pop()

    # Check for collisions
    check_collisions(snake)

    # Schedule the next turn
    window.after(SPEED, next_turn, snake, food)

def change_direction(event):
    global direction
    if event.keysym == "Up" and direction != "down":
        direction = "up"
    elif event.keysym == "Down" and direction != "up":
        direction = "down"
    elif event.keysym == "Left" and direction != "right":
        direction = "left"
    elif event.keysym == "Right" and direction != "left":
        direction = "right"


def check_collisions(snake):
    # Check if the snake collides with itself
    head_coords = snake.coordinates[0]
    body_coords = snake.coordinates[1:]
    if head_coords in body_coords:
        game_over()




def reset_game():
    global snake, food, score, direction

    # Reset the snake
    snake = Snake()
    # Reset the food
    food = Food()
    # Reset the score
    score = 0
    label.config(text="Score:{}".format(score))
    # Reset the direction
    direction = "Down"

    # Clear the canvas
    canvas.delete("all")

    # Start the game again
    next_turn(snake, food)


import time

# ...

def game_over():
    global direction

    # Flash the snake's body in red for a few iterations (faster animation)
    for _ in range(6):
        for square in snake.squares:
            canvas.itemconfig(square, fill="red")
        window.update()
        time.sleep(0.1)  # Adjust the sleep duration for faster animation
        for square in snake.squares:
            canvas.itemconfig(square, fill=SNAKE_COLOR)
        window.update()
        time.sleep(0.1)  # Adjust the sleep duration for faster animation

    # Stop the game
    direction = ""  # Disable the snake's movement

    # Prompt the player with a suggestion dialog
    choice = messagebox.askquestion("Game Over", "Play again?")
    if choice == "yes":
        reset_game()
    else:
        window.quit()



def show_game_over_message():
    # Prompt the player with a suggestion dialog
    choice = messagebox.askquestion("Game Over", "Play again?")
    if choice == "yes":
        reset_game()
    else:
        refresh_button = Button(window, text="Refresh", command=reset_game)
        label.pack(side="left")
        refresh_button.pack(side="left")




def game_over():
    global direction

    # Flash the snake's body in red for a few iterations
    for _ in range(6):
        for square in snake.squares:
            canvas.itemconfig(square, fill="red")
        window.update()
        time.sleep(0.2)
        for square in snake.squares:
            canvas.itemconfig(square, fill=SNAKE_COLOR)
        window.update()
        time.sleep(0.2)

    # Stop the game
    direction = ""  # Disable the snake's movement

    # Create a refresh button
    refresh_button = Button(window, text="Refresh", command=reset_game)
    refresh_button.pack()

    # Add your additional game over logic here
    # For example, you can display a game over message or perform any other actions


# Rest of your code...




window = Tk()
window.title("RINO")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text="Score:{}".format(score), font=('Arial', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Bind the arrow key presses to the change_direction function
window.bind("<Up>", change_direction)
window.bind("<Down>", change_direction)
window.bind("<Left>", change_direction)
window.bind("<Right>", change_direction)

window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+{int(x)}+{int(y)}")

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()


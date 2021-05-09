#python game

import time, random
from sense_hat import SenseHat

print("Snake game 20210509")

sense = SenseHat()

DIR_NONE = [0, 0]
DIR_UP = [0, -1]
DIR_RIGHT = [1, 0]
DIR_DOWN = [0, 1]
DIR_LEFT = [-1, 0]

RED = (255, 0 , 0)
WHITE = (255, 255, 255)
CLEAR = (0, 0, 0)

snake = [[3, 3]]
dir   = [1, 0]
snake_len   = 1

food_pos = [random.randint(0, 7), random.randint(0, 7)]

pixels = [CLEAR]*64

sense.clear()

def setDiection(new_dir): # 0=up, 1=right, 2=down, 3=left
    
    global dir

    if new_dir == DIR_NONE:
        return

    if new_dir == DIR_DOWN and dir == DIR_UP:
        print("ignore down")
        return
    
    if new_dir == DIR_UP and dir == DIR_DOWN:
        print("ignore up")
        return

    if new_dir == DIR_RIGHT and dir == DIR_LEFT:
        print("ignore right")
        return
    
    if new_dir == DIR_LEFT and dir == DIR_RIGHT:
        print("ignore left")
        return

    dir  = new_dir


def get_stick_state():

    for event in sense.stick.get_events():
        if event.action == "pressed":
            if event.direction == "up":
                return DIR_UP
            elif event.direction =="right":
                return DIR_RIGHT
            elif event.direction =="down":
                return DIR_DOWN
            elif event.direction =="left":
                return DIR_LEFT
    
    return DIR_NONE

def move_snake():

    global food_pos
    global snake_len
    global snake
    global dir
    
    snake.insert(0, [snake[0][0]+dir[0], snake[0][1] + dir[1] ])
    
    snake[0][0]  = ( snake[0][0] + 8 ) % 8
    snake[0][1]  = ( snake[0][1] + 8 ) % 8

    if snake[0] == food_pos:
        print("snake eats food")
        food_pos = []
        while food_pos == []:
            food_pos = [random.randint(0, 7), random.randint(0, 7)]
            if food_pos in snake:
                food_pos = []
        snake_len += 1
    
    if snake[0] in snake[1:]:
        snake_len = 1

    while len(snake) > snake_len:
        snake.pop()
    
    pixels = [CLEAR]*64

    pixels[food_pos[1] * 8 + food_pos[0]] = RED

    for pos in snake:
        pixels[ pos[1]*8 + pos[0] ] = WHITE
    
    sense.set_pixels(pixels)


while True:
    #print("stick state ", get_stick_state())
    
    setDiection(get_stick_state())

    move_snake()
    
    time.sleep(0.2)



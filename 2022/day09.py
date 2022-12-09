import math
import time
import platform
import subprocess

global field_min_x
global field_max_x
global field_min_y
global field_max_y

#########################################################################################################
# ASCII Visualization


# Clear Screen
def clear_screen():
    command = "cls" if platform.system().lower()=="windows" else "clear"
    return subprocess.call(command) == 0


# Adjust Edges of Playfield based on rope
def maintain_edges(rope):

    global field_min_x
    global field_max_x
    global field_min_y
    global field_max_y

    for i in range(len(rope)):
        x,y = rope[i]
        if x > field_max_x:
            field_max_x = x
        if x < field_min_x:
            field_min_x = x
        if y > field_max_y:
            field_max_y = y
        if y < field_min_y:
            field_min_y = y
    return


# Simple visualization
def show_field(move, steps, rope):

    line = ''
    maintain_edges(rope)
    clear_screen()
    print(move, steps)
    for y in range(field_min_y, field_max_y):
        for x in range(field_min_x, field_max_x):
            cell = '-'
            if rope[0] == (x, y):
                cell = 'H'
            else:
                for i in range(1, len(rope)):
                    if rope[i] == (x,y):
                        cell = 'T'
            line += cell
        print(line)
        line = ''
    time.sleep(0.01)

#########################################################################################################
# TUPLE HELPER


def tuples_add(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]


def tuples_subtract(t1, t2):
    return t1[0] - t2[0], t1[1] - t2[1]


def norm_direction(t1, t2):
    xx = 0
    yy = 0

    if (t1[0] - t2[0]) > 0:
        xx = 1
    elif (t1[0] - t2[0]) == 0:
        xx = 0
    else:
        xx = -1

    if (t1[1] - t2[1]) > 0:
        yy = 1
    elif (t1[1] - t2[1]) == 0:
        yy = 0
    else:
        yy = -1

    return xx,yy


def tuples_distance(t1, t2):
    return math.dist(t1,t2)

#########################################################################################################


def do_move(rope, move, steps, tail_trail, display=False):

    # Move Decoder
    moves = {
        'U': ( 0,-1),
        'D': ( 0, 1),
        'L': (-1, 0),
        'R': ( 1, 0)}

    # Iterate all steps of a moce
    for _ in range(steps):

        # Move Head
        start = rope[0]
        rope[0] = tuples_add(rope[0], moves[move])

        # Move Tail elementwise - if distance is more than 2 move otherwise remain
        for j in range(1, len(rope)):
            dist = tuples_distance(rope[j-1], rope[j])
            if dist >= 2:
                rope[j] = tuples_add(rope[j], norm_direction(rope[j-1], rope[j]))

        # Register Tail movement
        tail_trail.add(rope[len(rope) - 1])

        # Display moves if specified
        if display:
            show_field(move, steps, rope)

    return rope, tail_trail


def runner(rope_length, show=False):

    # Init variables
    tail_trail = {(0, 0)}
    rope = []
    length = rope_length

    for i in range(length):
        rope.append((0, 0))

    # Open File with move commands
    with open(fn) as f:
        data = f.readlines()

    # Perform moves
    for move in data:
        move, steps = move.split()
        rope, tail_trail = do_move(rope, move, int(steps), tail_trail, show)

    return tail_trail


# Perform tasks
if __name__ == '__main__':

    fn = r"../local/day09.txt"

    field_min_x = -10
    field_max_x = 10
    field_min_y = -10
    field_max_y = 10

    tail_trail = runner(2)
    print(len(tail_trail))

    tail_trail = runner(10)
    print(len(tail_trail))

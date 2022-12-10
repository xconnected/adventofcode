import math
import time
import platform
import subprocess


def cycler(cycle, cycle_trigger):
    cycle += 1
    cycle_trigger -= 1

    if cycle_trigger == 0:
        do_calc = True
        cycle_trigger = 40
    else:
        do_calc = False

    return cycle, cycle_trigger, do_calc


def run_signal_detector(dprogram, debug=False):
    # Init variables
    register_x = 1
    cycle_counter, cycle_trigger, _ = cycler(0, 20)

    signal_strength = 0

    # Open File with program
    with open(fn) as f:
        program = f.readlines()

    # Execute
    for cmdline in program:

        cycle_counter, cycle_trigger, do_calc = cycler(cycle_counter, cycle_trigger)

        if do_calc:
            signal_strength += cycle_counter * register_x

        if debug:
            print(cycle_counter, register_x, signal_strength)

        if cmdline.startswith('addx'):
            _, param = cmdline.split()
            register_x += int(param)
            cycle_counter, cycle_trigger, do_calc = cycler(cycle_counter, cycle_trigger)

            if do_calc:
                signal_strength += cycle_counter * register_x

            if debug:
                print(cycle_counter, register_x, signal_strength)

    return register_x, signal_strength



def run_visualization(program, debug=False):

    # Init
    cycle_counter = 1
    cycle_event = 1
    pixel_col = 0
    register_x = 1
    program_counter = 0
    param = 0
    stop = False

    display_line = ''

    # Execute per cycle
    while True:

        if cycle_counter >= cycle_event:
            register_x += int(param)
            if program[program_counter].startswith('addx'):
                _, param = program[program_counter].split()
                cycle_event = cycle_counter + 2
            else:
                cycle_event = cycle_counter + 1
                param = 0

            if program_counter >= len(program)-1:
                stop = True
            else:
                stop = False
                program_counter += 1

        if register_x-1 <= pixel_col <= register_x+1:
            display_line += '#'
        else:
            display_line += '.'

        # Start of optional Debug Code
        if debug:
            if register_x <= 0:
                print('data  : ', register_x, register_x-1 <= pixel_col <= register_x+1)
                print('sprite: ' + '###' + '.' * 37)
                print('CRT row: ' + display_line)
            else:
                print('data  : ', register_x, register_x-1 <= pixel_col <= register_x+1)
                print('sprite : ' + '.' * (register_x - 1) + '###' + '.' * (41 - register_x - 3))
                print('CRT row: ' + display_line)
        # End of optional Debug Code

        if pixel_col >= 39:
            print(display_line)
            pixel_col = 0
            display_line = ''
        else:
            pixel_col += 1

        cycle_counter += 1

        if stop:
            break

    return program_counter, cycle_counter


# Perform tasks
if __name__ == '__main__':

    fn = r"../local/day10.txt"

    with open(fn) as f:
        program = f.readlines()

    print(run_signal_detector(program))
    print(run_visualization(program))

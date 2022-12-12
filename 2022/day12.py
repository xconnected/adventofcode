import sys
import numpy as np


def load_area(fn):

    global area

    file = open(fn, 'r')

    area_lines = file.readlines()

    init = True
    for line in area_lines:
        if init:
            area = np.vstack([list(line.strip())])
            init = False
        else:
            area = np.vstack([area, list(line.strip())])


def find(search_value):

    global area

    x_max, y_max = area.shape

    hit_x = 0
    hit_y = 0

    for y in range(0, y_max):
        for x in range(0, x_max):
            if area[x,y] == search_value:
                hit_x = x
                hit_y = y

    return hit_x, hit_y


def check_and_set_around(x, y):

    spot = area[x,y]
    step = route[x,y] + 1

    # left
    if y > 0:
        if int(route[x, y-1]) == 0 or route[x,y-1] >= step:
            if abs(ord(spot) - ord(area[x, y-1])) <= 1:
                route[x, y-1] = step
                check_and_set_around(x, y-1)

    # right
    if y < area.shape[1]-1:
        if int(route[x, y+1]) == 0  or route[x,y+1] >= step:
            if abs(ord(spot) - ord(area[x, y+1])) <= 1:
                route[x, y+1] = step
                check_and_set_around(x, y+1)

    # up
    if x > 0:
        if int(route[x-1, y]) == 0 or route[x-1,y] >= step:
            if abs(ord(spot) - ord(area[x-1, y])) <= 1:
                route[x-1, y] = step
                check_and_set_around(x-1, y)

    # down
    if x < area.shape[0]-1:
        if int(route[x+1, y]) == 0 or route[x+1,y] >= step:
            if abs(ord(spot) - ord(area[x+1, y])) <= 1:
                route[x+1, y] = step
                check_and_set_around(x+1, y)

    return area, route


if __name__ == '__main__':

    print("This approach never finished on the large example but on all tests.")
    fn = r"../local/day12.txt"

    load_area(fn)
    route = np.zeros(area.shape, dtype=int)
    print(area)

    xE,yE = find('E')
    route[xE,yE] = 1
    area[xE, yE] = 'z'

    xS,yS = find('S')
    area[xS, yS] = 'a'

    check_and_set_around(xE, yE)

    if xS >= 0:
        print("1: ", route[xS-1, yS])

    if yS <= route.shape[1]-1:
        print("2: ", route[xS, yS+1])

    if xS <= route.shape[0]-1:
        print("3: ", route[xS+1, yS])

#!/usr/bin/evn python3

'''
Generates an incomplete representation of the Mandelbrot set.
https://en.wikipedia.org/wiki/Mandelbrot_set
'''

import functools
import time
import matplotlib.pyplot as plt
import numpy as np


def time_this(func):
    '''Execution time decorator.'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Execution time {func.__name__}(): {end - start}')
        return result
    return wrapper


@time_this
def make_mandelbrot():
    '''Approximate the mandelbrot set without using complex numbers.
    The effort of incorporating complex numbers is currently unknown, as is
    their effect on calculation time.
    '''
    # Increase pixel_amount_sqrt and max_iteration to increase image clarity.
    # The linspace() boundaries roughly set the correct problem space.
    pixel_amount_sqrt = 220
    x_coords = np.linspace(-2.00, 0.47, pixel_amount_sqrt)
    y_coords = np.linspace(-1.12, 1.12, pixel_amount_sqrt)
    valid_x = []
    valid_y = []
    for x_coord in x_coords:
        for y_coord in y_coords:
            x = 0.0
            y = 0.0
            iteration = 0
            max_iteration = 800
            while (x * x + y * y) <= 4 and iteration < max_iteration:
                x_temp = (x * x) - (y * y) + x_coord
                y = (2 * x * y) + y_coord
                x = x_temp
                iteration += 1
            if (x * x + y * y) <= 4:
                valid_x.append(x_coord)
                valid_y.append(y_coord)

        plt.scatter(valid_x, valid_y, marker=',', s=1)


make_mandelbrot()

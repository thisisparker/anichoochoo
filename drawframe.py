#!/usr/bin/env python3
# For now, render a single frame of a @choochoobot drawing onto a canvas.
# More to come.

import errno
import random
import os

from PIL import Image

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 576
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
NUMROWS = 6
BLOCK_SIDE = int(SCREEN_HEIGHT / NUMROWS)
BLOCK_SIZE = (BLOCK_SIDE, BLOCK_SIDE)
ROW_YS = [BLOCK_SIDE * x for x in range(NUMROWS)]
FRAME_COUNT = 1080
OUTPUT_DIR = 'slides'

choochoo = Image.open("images/choochoo.png").resize(BLOCK_SIZE)
redcar = Image.open("images/redcar.png").resize(BLOCK_SIZE)
greencar = Image.open("images/greencar.png").resize(BLOCK_SIZE)
cactus = Image.open("images/cactus.png").resize(BLOCK_SIZE)
palm = Image.open("images/palm.png").resize(BLOCK_SIZE)
turtle = Image.open("images/turtle.png").resize(BLOCK_SIZE)
horse = Image.open("images/horse.png").resize(BLOCK_SIZE)
sun = Image.open("images/sun.png").resize(BLOCK_SIZE)
moon = Image.open("images/moon.png").resize(BLOCK_SIZE)
blank = Image.new("RGBA", BLOCK_SIZE, (0, 0, 0, 0))


def main():

    # Create the output directory if it doesn't already exist
    try:
        os.makedirs(OUTPUT_DIR)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    # "static" holds the elements that do not change throughout the animation.
    # That includes the train and its cars.

    static = Image.new('RGBA', SCREEN_SIZE, (0, 0, 0, 0))

    choochx = int(BLOCK_SIDE * 6)
    choochy = ROW_YS[3]
    place_engine(static, choochx, choochy)

    train_length = 7

    carx = choochx

    for car in range(train_length):
        carx = carx + BLOCK_SIDE
        place_car(static, carx, choochy)

    # "sky_row" is a long strip that has one sun and moon, advancing slowly.

    sky_row = Image.new('RGBA', (2 * SCREEN_WIDTH, BLOCK_SIDE), (0, 0, 0, 0))
    sky_row.paste(sun, (SCREEN_WIDTH, 0), sun)
    sky_row.paste(moon, (0, 0), moon)

    # Each item in the "minutes" list is a frame on which the sky_row advances.

    minutes = [int(FRAME_COUNT / 40 * _) for _ in range(1, 40)]

    sky_offset = SCREEN_WIDTH

    # Create row objects for each of the rows in the background.
    # The class starts with an image and takes a parallax factor.

    row1 = Background_row(ROW_YS[1], 0.2)
    row2 = Background_row(ROW_YS[2], 0.3)
    row4 = Background_row(ROW_YS[4], 0.4)
    row5 = Background_row(ROW_YS[5], 0.6)

    BG_ROWS = [row1, row2, row4, row5]

    frame_number = 0

    for frame_number in range(1, FRAME_COUNT + 1):

        bgcolor = (255, 255, 255)

        render = Image.new('RGBA', SCREEN_SIZE, bgcolor)

        bounce = random.randint(-4, 4)
        render.paste(static, (0, bounce), static)

        render.paste(sky_row, (-sky_offset, 0), sky_row)
        if frame_number in minutes:
            sky_offset -= BLOCK_SIDE

        for row in BG_ROWS:
            if row.offset <= 0:
                row.img = row.img.crop((0, 0, SCREEN_WIDTH, BLOCK_SIDE))
                new_row = Image.new('RGBA', (SCREEN_WIDTH, BLOCK_SIDE), (0, 0, 0, 0))
                place_scenery(new_row, 0)
                combined_row = Image.new('RGBA', (2 * SCREEN_WIDTH, BLOCK_SIDE), (0, 0, 0, 0))
                combined_row.paste(new_row, (0, 0), new_row)
                combined_row.paste(row.img, (SCREEN_WIDTH, 0), row.img)
                row.img = combined_row
                row.offset = SCREEN_WIDTH

            render.paste(row.img, (-row.offset, row.y), row.img)

            row.offset = int(row.offset - BLOCK_SIDE * row.parallax)

        new_filename = OUTPUT_DIR + "/img" + format(frame_number, "04d") + ".png"
        print("rendering frame " + str(frame_number) + " as " + new_filename)
        render.save(new_filename)

        frame_number += 1


def place_engine(canvas, x, y):
    canvas.paste(choochoo, (x, y), choochoo)


def place_car(canvas, x, y):
    cars = [redcar, greencar]
    car = random.choice(cars)
    canvas.paste(car, (x, y), car)


def place_scenery(canvas, y):
    x = 0
    for block in range(int(canvas.width)):
        if random.randint(1, 10) == 1:
            thing = random.choice([cactus, cactus, palm, palm, horse, turtle])
            canvas.paste(thing, (x, y), thing)
        x += BLOCK_SIDE


class Background_row:
    def __init__(self, yvalue, parallax):
        self.y = yvalue
        self.img = Image.new('RGBA', (2 * SCREEN_WIDTH, BLOCK_SIDE), (0, 0, 0, 0))
        place_scenery(self.img, 0)
        self.offset = SCREEN_WIDTH
        self.parallax = parallax

if __name__ == "__main__":
    main()

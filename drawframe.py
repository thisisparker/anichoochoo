#!/usr/bin/env python3
# For now, render a single frame of a @choochoobot drawing onto a canvas.
# More to come.

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
IMAGE_DIR = 'images'


def load_block_image(name):
    return Image.open(os.path.join(IMAGE_DIR, name)).resize(BLOCK_SIZE)


def load_all_block_images(names):
    return [load_block_image(name) for name in names]

things = load_all_block_images(["cactus.png", "cactus.png",
                                "palm.png", "palm.png",
                                "horse.png",
                                "turtle.png"])
blank = Image.new("RGBA", BLOCK_SIZE, (0, 0, 0, 0))


class Drawable:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Sprite(Drawable):
    def __init__(self, x, y, image):
        super(Sprite, self).__init__(x, y)
        if isinstance(image, str):
            self.image = load_block_image(image)
        else:
            self.image = image

    def draw(self, canvas):
        canvas.paste(self.image, (self.x, self.y), self.image)


class Engine(Sprite):
    def __init__(self, x, y):
        super(Engine, self).__init__(x, y, "choochoo.png")


class Car(Sprite):
    cars = load_all_block_images(["redcar.png", "greencar.png"])

    def __init__(self, x, y):
        super(Car, self).__init__(x, y, random.choice(self.cars))


class Sun(Sprite):
    def __init__(self, x, y):
        super(Sun, self).__init__(x, y, "sun.png")


class Moon(Sprite):
    def __init__(self, x, y):
        super(Moon, self).__init__(x, y, "moon.png")


def place_scenery(canvas, y):
    x = 0
    for block in range(int(canvas.width)):
        if random.randint(1, 10) == 1:
            thing = random.choice(things)
            canvas.paste(thing, (x, y), thing)
        x += BLOCK_SIDE


class Background_row:
    def __init__(self, yvalue, parallax):
        self.y = yvalue
        self.img = Image.new('RGBA',
                             (2 * SCREEN_WIDTH, BLOCK_SIDE),
                             (0, 0, 0, 0))
        place_scenery(self.img, 0)
        self.offset = SCREEN_WIDTH
        self.parallax = parallax


def main():
    # Create the output directory if it doesn't already exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # "static" holds the elements that do not change throughout the animation.
    # That includes the train and its cars.

    static = Image.new('RGBA', SCREEN_SIZE, (0, 0, 0, 0))

    choochx = int(BLOCK_SIDE * 6)
    choochy = ROW_YS[3]
    Engine(choochx, choochy).draw(static)

    train_length = 7

    for car in range(train_length):
        Car(choochx + (car + 1) * BLOCK_SIDE, choochy).draw(static)

    # "sky_row" is a long strip that has one sun and moon, advancing slowly.

    sky_row = Image.new('RGBA', (2 * SCREEN_WIDTH, BLOCK_SIDE), (0, 0, 0, 0))
    Sun(SCREEN_WIDTH, 0).draw(sky_row)
    Moon(0, 0).draw(sky_row)

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
                new_row = Image.new('RGBA',
                                    (SCREEN_WIDTH, BLOCK_SIDE),
                                    (0, 0, 0, 0))
                place_scenery(new_row, 0)
                combined_row = Image.new('RGBA',
                                         (2 * SCREEN_WIDTH, BLOCK_SIDE),
                                         (0, 0, 0, 0))
                combined_row.paste(new_row, (0, 0), new_row)
                combined_row.paste(row.img, (SCREEN_WIDTH, 0), row.img)
                row.img = combined_row
                row.offset = SCREEN_WIDTH

            render.paste(row.img, (-row.offset, row.y), row.img)

            row.offset = int(row.offset - BLOCK_SIDE * row.parallax)

        new_filename = os.path.join(OUTPUT_DIR, "img%04d.png" % frame_number)
        print("rendering frame %d as %s" % (frame_number, new_filename))
        render.save(new_filename)

if __name__ == "__main__":
    main()

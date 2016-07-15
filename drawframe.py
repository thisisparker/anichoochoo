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
BLOCK_SIDE = SCREEN_HEIGHT // NUMROWS
BLOCK_SIZE = (BLOCK_SIDE, BLOCK_SIDE)
ROW_YS = range(0, SCREEN_HEIGHT, BLOCK_SIDE)
FRAME_COUNT = 1080
OUTPUT_DIR = 'slides'
IMAGE_DIR = 'images'
BGCOLOR = (255, 255, 255)
TRAIN_LENGTH = 7


def load_block_image(name):
    return Image.open(os.path.join(IMAGE_DIR, name)).resize(BLOCK_SIZE)


def load_all_block_images(names):
    return [load_block_image(name) for name in names]


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


class Sky(Sprite):
    '''This is a long strip that has one sun and moon, advancing slowly.'''
    def __init__(self):
        sky = Image.new('RGBA', (2 * SCREEN_WIDTH, BLOCK_SIDE), (0, 0, 0, 0))
        Sun(SCREEN_WIDTH, 0).draw(sky)
        Moon(0, 0).draw(sky)
        super(Sky, self).__init__(-SCREEN_WIDTH, 0, sky)

    def move_right(self):
        self.x += BLOCK_SIDE


class BackgroundRow(Drawable):
    '''This is a row of background items that moves right every frame.
    The row moves faster or slower depending on the parallax argument.
    Once the row has moved past the edge of the screen, additional items
    are drawn on an extended, shifted copy of the image.'''
    things = load_all_block_images(["cactus.png", "cactus.png",
                                    "palm.png", "palm.png",
                                    "horse.png",
                                    "turtle.png"])

    def __init__(self, y, parallax):
        super(BackgroundRow, self).__init__(-SCREEN_WIDTH, y)
        self.image = Image.new('RGBA',
                               (2 * SCREEN_WIDTH, BLOCK_SIDE),
                               (0, 0, 0, 0))
        self.place_scenery(self.image, 0)
        self.parallax = parallax

    @classmethod
    def place_scenery(self, canvas, y):
        for x in range(0, canvas.width, BLOCK_SIDE):
            if random.randint(1, 10) == 1:
                thing = random.choice(self.things)
                canvas.paste(thing, (x, y), thing)

    def move_right(self):
        self.x += BLOCK_SIDE * self.parallax

        if self.x >= 0:
            self.image = self.image.crop((0, 0, SCREEN_WIDTH, BLOCK_SIDE))
            new_row = Image.new('RGBA',
                                (SCREEN_WIDTH, BLOCK_SIDE),
                                (0, 0, 0, 0))
            self.place_scenery(new_row, 0)
            combined_row = Image.new('RGBA',
                                     (2 * SCREEN_WIDTH, BLOCK_SIDE),
                                     (0, 0, 0, 0))
            combined_row.paste(new_row, (0, 0), new_row)
            combined_row.paste(self.image, (SCREEN_WIDTH, 0), self.image)
            self.image = combined_row
            self.x -= SCREEN_WIDTH

    def draw(self, canvas):
        canvas.paste(self.image, (int(self.x), self.y), self.image)


class Train(Drawable):
    def __init__(self, x, y):
        super(Train, self).__init__(x, y)
        self.image = Image.new('RGBA', SCREEN_SIZE, (0, 0, 0, 0))
        Engine(0, 0).draw(self.image)
        for car in range(TRAIN_LENGTH):
            Car((car + 1) * BLOCK_SIDE, 0).draw(self.image)

    def draw(self, canvas):
        bounce = random.randint(-4, 4)
        canvas.paste(self.image, (self.x, self.y + bounce), self.image)


def main():
    # Create the output directory if it doesn't already exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # "sky" is a long strip that has one sun and moon, advancing slowly.
    sky = Sky()

    # Each item in the "minutes" list is a frame on which the sky_row advances.
    minutes = range(FRAME_COUNT // 40, FRAME_COUNT, FRAME_COUNT // 40)

    # Create row objects for each of the rows in the background.
    # The class starts with an image and takes a parallax factor.
    bg_rows = [
        BackgroundRow(ROW_YS[1], 0.2),
        BackgroundRow(ROW_YS[2], 0.3),
        BackgroundRow(ROW_YS[4], 0.4),
        BackgroundRow(ROW_YS[5], 0.6),
    ]

    train = Train(BLOCK_SIDE * 6, ROW_YS[3])

    for frame_number in range(1, FRAME_COUNT + 1):
        render = Image.new('RGBA', SCREEN_SIZE, BGCOLOR)
        train.draw(render)
        sky.draw(render)
        if frame_number in minutes:
            sky.move_right()

        for row in bg_rows:
            row.draw(render)
            row.move_right()

        new_filename = os.path.join(OUTPUT_DIR, "img%04d.png" % frame_number)
        print("rendering frame %d as %s" % (frame_number, new_filename))
        render.save(new_filename)

if __name__ == "__main__":
    main()

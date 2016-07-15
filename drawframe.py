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


class BackgroundRow(Drawable):
    things = load_all_block_images(["cactus.png", "cactus.png",
                                    "palm.png", "palm.png",
                                    "horse.png",
                                    "turtle.png"])

    def __init__(self, y, parallax):
        super(BackgroundRow, self).__init__(-SCREEN_WIDTH, y)
        self.img = Image.new('RGBA',
                             (2 * SCREEN_WIDTH, BLOCK_SIDE),
                             (0, 0, 0, 0))
        self.place_scenery(self.img, 0)
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
            self.img = self.img.crop((0, 0, SCREEN_WIDTH, BLOCK_SIDE))
            new_row = Image.new('RGBA',
                                (SCREEN_WIDTH, BLOCK_SIDE),
                                (0, 0, 0, 0))
            self.place_scenery(new_row, 0)
            combined_row = Image.new('RGBA',
                                     (2 * SCREEN_WIDTH, BLOCK_SIDE),
                                     (0, 0, 0, 0))
            combined_row.paste(new_row, (0, 0), new_row)
            combined_row.paste(self.img, (SCREEN_WIDTH, 0), self.img)
            self.img = combined_row
            self.x -= SCREEN_WIDTH

    def draw(self, canvas):
        canvas.paste(self.img, (int(self.x), self.y), self.img)


def main():
    # Create the output directory if it doesn't already exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # "static" holds the elements that do not change throughout the animation.
    # That includes the train and its cars.
    static = Image.new('RGBA', SCREEN_SIZE, (0, 0, 0, 0))
    choochx = BLOCK_SIDE * 6
    choochy = ROW_YS[3]
    Engine(choochx, choochy).draw(static)
    for car in range(TRAIN_LENGTH):
        Car(choochx + (car + 1) * BLOCK_SIDE, choochy).draw(static)

    # "sky_row" is a long strip that has one sun and moon, advancing slowly.
    sky_row = Image.new('RGBA', (2 * SCREEN_WIDTH, BLOCK_SIDE), (0, 0, 0, 0))
    Sun(SCREEN_WIDTH, 0).draw(sky_row)
    Moon(0, 0).draw(sky_row)

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

    sky_offset = SCREEN_WIDTH
    for frame_number in range(1, FRAME_COUNT + 1):
        render = Image.new('RGBA', SCREEN_SIZE, BGCOLOR)
        bounce = random.randint(-4, 4)
        render.paste(static, (0, bounce), static)
        render.paste(sky_row, (-sky_offset, 0), sky_row)
        if frame_number in minutes:
            sky_offset -= BLOCK_SIDE

        for row in bg_rows:
            row.draw(render)
            row.move_right()

        new_filename = os.path.join(OUTPUT_DIR, "img%04d.png" % frame_number)
        print("rendering frame %d as %s" % (frame_number, new_filename))
        render.save(new_filename)

if __name__ == "__main__":
    main()

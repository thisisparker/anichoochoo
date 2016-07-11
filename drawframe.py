#!/usr/bin/env python3
# For now, render a single frame of a @choochoobot drawing onto a canvas.
# More to come.

from PIL import Image
import errno
import os
import random
from math import ceil

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 576
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
NUMROWS = 6
BLOCK_SIDE = int(SCREEN_HEIGHT/NUMROWS)
BLOCK_SIZE = (BLOCK_SIDE,BLOCK_SIDE)
ROWS = [BLOCK_SIDE * x for x in range(NUMROWS)]
FRAME_COUNT = 160
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
blank = Image.new("RGBA",BLOCK_SIZE,(0,0,0,0))

def main():

    # Create the output directory if it doesn't already exist
    try:
        os.makedirs(OUTPUT_DIR)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    # "static" holds the elements that do not change throughout the animation.
    # That includes the train and its cars.

    static = Image.new('RGBA',SCREEN_SIZE,(0,0,0,0))

    choochx = int(BLOCK_SIDE * 6)
    choochy = ROWS[3]
    place_engine(static,choochx,choochy)

    train_length = 7

    carx = choochx

    for car in range(train_length):
        carx = carx + BLOCK_SIDE
        place_car(static,carx,choochy)

    # "sky_row" is a long strip that has one sun and moon, advancing slowly.

    sky_row = Image.new('RGBA',(2 * SCREEN_WIDTH,BLOCK_SIDE),(0,0,0,0))
    sky_row.paste(sun,(SCREEN_WIDTH,0),sun)
    sky_row.paste(moon,(0,0),moon)

    # Each item in the "minutes" list is a frame on which the sky_row advances.

    minutes = [int(FRAME_COUNT/40 * _) for _ in range(1,40)] 

    sky_offset = SCREEN_WIDTH

    # Start with one frame full of scenery, and set the offset to zero. It'll create more along the way.

    scenery = Image.new('RGBA',SCREEN_SIZE,(0,0,0,0))
    for row in [ROWS[1],ROWS[2],ROWS[4],ROWS[5]]:
        place_scenery(scenery,row)
    offset = 0

    frame_number = 0

    while frame_number <= FRAME_COUNT:

        bgcolor = (255,255,255)

        render = Image.new('RGBA',SCREEN_SIZE,bgcolor)

        bounce = random.randint(-4,4)
        render.paste(static,(0,bounce),static)

        render.paste(sky_row,(-sky_offset,0),sky_row)
        if frame_number in minutes:
            sky_offset -= BLOCK_SIDE

        if offset == 0:
            scenery = scenery.crop((0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
            new_scene = Image.new('RGBA',SCREEN_SIZE,(0,0,0,0))
            for row in [ROWS[1],ROWS[2],ROWS[4],ROWS[5]]:
                place_scenery(new_scene,row)
            combined_scene = Image.new('RGBA',(2 * SCREEN_WIDTH,SCREEN_HEIGHT),(0,0,0,0))
            combined_scene.paste(new_scene,(0,0),new_scene)
            combined_scene.paste(scenery,(SCREEN_WIDTH,0),scenery)
            scenery = combined_scene
            offset = SCREEN_WIDTH

        render.paste(scenery,(-offset,0),scenery)
        
        new_filename = OUTPUT_DIR + "/img" + format(frame_number,"04d") + ".png"
        print("rendering frame " + str(frame_number) + " as " + new_filename)
        render.save(new_filename)

        offset -= BLOCK_SIDE
        frame_number += 1


def place_engine(canvas,x,y):
    canvas.paste(choochoo,(x,y),choochoo)

def place_car(canvas,x,y):
    cars = [redcar,greencar]
    car = random.choice(cars)
    canvas.paste(car,(x,y),car)

def place_scenery(canvas,y):
    x = 0    
    for block in range(int(canvas.width)):
        if random.randint(1,10) == 1:
            thing = random.choice([cactus,cactus,palm,palm,horse,turtle])
            canvas.paste(thing,(x,y),thing)
        x += BLOCK_SIDE

if __name__ == "__main__":
    main()

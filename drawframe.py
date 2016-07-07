#!/usr/bin/env python3
# For now, render a single frame of a @choochoobot drawing onto a canvas.
# More to come.

from PIL import Image
import random, json
import glob, os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 576
NUMROWS = 6
BLOCK_SIDE = int(SCREEN_HEIGHT/NUMROWS)
BLOCK_SIZE = (BLOCK_SIDE,BLOCK_SIDE)
ROWS = [BLOCK_SIDE * x for x in range(NUMROWS)]

choochoo = Image.open("images/choochoo.png").resize(BLOCK_SIZE)
redcar = Image.open("images/redcar.png").resize(BLOCK_SIZE)
greencar = Image.open("images/greencar.png").resize(BLOCK_SIZE)
cactus = Image.open("images/cactus.png").resize(BLOCK_SIZE)
sun = Image.open("images/sun.png").resize(BLOCK_SIZE)
blank = Image.new("RGBA",BLOCK_SIZE,(0,0,0,0))

def main():

    static = Image.new('RGBA',(SCREEN_WIDTH,SCREEN_HEIGHT),(255,255,255))

    static.paste(sun,(0,0),sun)

    # choochx = random.randint(0,SCREEN_WIDTH)
    choochx = int(BLOCK_SIDE * 6)
    choochy = ROWS[3]
    placechoochoo(static,choochx,choochy)

    # trainlength = random.randint(1,10)
    trainlength = 7

    carx = choochx

    for car in range(trainlength):
        carx = carx + BLOCK_SIDE
        placecar(static,carx,choochy)

    background = Image.new('RGBA',(6*SCREEN_WIDTH,SCREEN_HEIGHT),(0,0,0,0))

    for row in [ROWS[1],ROWS[2],ROWS[4],ROWS[5]]:
        placescenery(background,row)

    render = static.copy()

    offset = background.width - render.width

    img_suffix = 0

    while offset >= 0:
        render = static.copy()
        render.paste(background,(-offset,0),background)
        offset = offset - BLOCK_SIDE
        new_filename = "slides/img" + format(img_suffix,"03d") + ".png"
        render.save(new_filename)

        print("rendering " + new_filename)

        img_suffix += 1


def placechoochoo(canvas,x,y):
    canvas.paste(choochoo,(x,y),choochoo)

def placecar(canvas,x,y):
    if random.choice(["red","green"]) == "red":
        car = redcar
    else:
        car = greencar
    canvas.paste(car,(x,y),car)

def placescenery(canvas,y):
    x = 0    
    for block in range(int(canvas.width)):
        if random.randint(1,10) == 1:
            canvas.paste(cactus,(x,y),cactus)
        x = x + BLOCK_SIDE

if __name__ == "__main__":
    main()

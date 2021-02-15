from random import randrange
from struct import unpack

with open("/dev/fb1", "wb+") as fb:
    while True:
        i = randrange(480 * 320) * 2
        j = randrange(3)
        shift = [11, 5, 0][j]
        max = [31, 63, 31][j]
        fb.seek(i)
        px = unpack("H", fb.read(2))[0]
        color = (px >> shift) & max
        if color <= max - 16:
            color += 16

        color <<= shift
        px |= color
        #fb.seek(i)
        fb.write(px.to_bytes(2, "little"))
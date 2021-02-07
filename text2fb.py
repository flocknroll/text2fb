import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageColor, ImageFont

sRes = (120, 80)
oRes = (480, 320)


def px24_to_16(r, g, b):
    r >>= 3
    g >>= 2
    b >>= 3
    return ((r << 11) + (g << 5) + b).to_bytes(2, "little")

def rgb24_to_rgb16(bmp):
    bBuffer = memoryview(bmp)
    outBuffer = bytearray(oRes[0] * oRes[1] * 2)

    for i in range(oRes[0] * oRes[1]):
        r = bBuffer[i * 3]     
        g = bBuffer[i * 3 + 1]
        b = bBuffer[i * 3 + 2]

        if r + g + b == 0:
            px = b"\x00\x00"
        elif r + g + b == 768:
            px = b"\xff\xff"
        else:
            px = px24_to_16(r, g, b)

        outBuffer[i * 2] = px[0]
        outBuffer[i * 2 + 1] = px[1]

    return outBuffer


def np_rgb24_to_rgb16(bmp):
    bBuffer = memoryview(bmp)
    na = np.array(bBuffer, dtype="uint16").reshape((oRes[0] * oRes[1], 3))
    arrays = np.hsplit(na, 3)
    r = arrays[0]
    g = arrays[1]
    b = arrays[2]
    np.right_shift(r, 3, out=r)
    np.left_shift(r, 11, out=r)
    np.right_shift(g, 2, out=g)
    np.left_shift(g, 5, out=g)
    np.right_shift(b, 3, out=b)

    na = r + g + b

    return na.tobytes()


def text_to_fb(text):
    im = Image.new("RGB", sRes)

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("/usr/share/fonts/TTF/Inconsolata-Regular.ttf", size=42)
    w, h = font.getsize(text)

    x = (sRes[0] - w) // 2
    y = (sRes[1] - h) // 2 
    draw.text((x, y), text, font=font, fill=ImageColor.getrgb("red"))
    #draw.text((x, y), hour, font=font, fill=(32, 20, 32))

    im = im.resize(oRes, Image.NEAREST)

    fbBuffer = np_rgb24_to_rgb16(im.tobytes())

    with open("/dev/fb1", "wb") as fb:
        fb.write(fbBuffer)

def show_hour():
    hour = datetime.strftime(datetime.now(), "%H:%M")
    text_to_fb(hour)

show_hour()
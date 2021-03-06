# -*-- coding = utf-8 --*-

import math
import random
import string
import sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter

# the position of fontsize
font_path  = '../Library/Fonts/simsun.ttc'

# generate code
number = 4

# background color
bgcolor = (255,255,255)

# font color
fontcolor = (255,0,0)

# size
size = (60,30)

# disturb color
linecolor = (0,0,255)

# add disturb color ?
draw_line = True

# thread line
line_number = (1,5)

def gene_text():
    source = []
    for i in range(number):
        source.append(str(random.randint(0,9)))
    '''
    source = list(string.letters)
    for index in range(10):
        source.append(str(index))
    '''
    return ''.join(random.sample(source,number))

def gene_line(draw,width,height):
    begin = (random.randint(0,width),random.randint(0,height))
    end = (random.randint(0,width),random.randint(0,height))
    draw.line([begin,end],fill=linecolor)

def gene_code():
    width,height = size
    image = Image.new('RGBA',(width,height),bgcolor)
    font = ImageFont.truetype(font_path,25)
    draw = ImageDraw.Draw(image)
    text = gene_text()
    print text
    font_width,font_height = font.getsize(text)
    draw.text(((width-font_width)/number,(height-font_height)/number),
              text,font=font,fill=fontcolor)
    if draw_line:
        gene_line(draw,width,height)
    #image = image.transform((width+20,height+10),Image.AFFINE,(1,-0.3,0,-0.1,1,0),
    #                        Image.BILINEAR)
    #image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    if random.random()<0.3:
        image.save('test/%s.bmp' % text)
    else:
        image.save('train/%s.bmp' % text)

if __name__ == '__main__':
    for idx in range(2000):
        gene_code()

import conventor_
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math

fumen = conventor_.fumen()
fumen.read('em.html')
data = fumen.data
long = fumen.find_long_press()
# decide the size of image
## find max in data column 9
max_mes = data.iloc[:, 9].max()
width = math.ceil(max_mes/4) * (134+32 + 25)
height = 128 * 4 + 100

# create image
def drawer(rail, mes, note, top):
    # load note image
    note_img_map = {
        0: 'pic/s.gif',
        1: 'pic/w.gif',
        2: 'pic/b.gif',        
        3: 'pic/w.gif',
        4: 'pic/b.gif',        
        5: 'pic/w.gif',
        6: 'pic/b.gif',        
        7: 'pic/w.gif',
        8: 'pic/t.gif'
    }
    rail_x = {
        0: 0,
        1: 36,
        2: 49,
        3: 62,
        4: 75,
        5: 88,
        6: 101,
        7: 114
    }
    if rail == 0: 
        if note == 1: note_img = Image.open('pic/s.gif')
        if note == -1: note_img = Image.open('pic/hhs.gif')
    if rail == 1 or rail == 3 or rail == 5 or rail == 7:
        if note == 1: note_img = Image.open('pic/w.gif')
        if note == -1: 
            note_img = Image.open('pic/hhw.gif')
    if rail == 2 or rail == 4 or rail == 6:
        if note == 1: note_img = Image.open('pic/b.gif')
        if note == -1: note_img = Image.open('pic/hhb.gif')
    # note_img = Image.open(note_img_map[rail])
    note_img = note_img.resize([note_img.size[0]*4, note_img.size[1]*4])

    # from mes and top, get x and y
    if rail <= 7:
        column = mes//4
        row = 3-mes%4
        x = column * (backsize_x + greysize_x) + (rail_x[rail] + rail)*4 # +rail 以居中
        y = row * (greysize_y) + (top-4)*4 # 储存时+4，所以要-4
    if rail == 8:
        column = mes//4
        row = 3-mes%4
        x = column * (backsize_x + greysize_x) + backsize_x + 4
        y = row * (greysize_y) + (top-2)*4
    return note_img, (x, y)

## variables
single_backsize_x = 134
single_backsize_y = 32

backsize_x = single_backsize_x*4
backsize_y = single_backsize_y*4
greysize_x = 32*4
greysize_y = backsize_y*4
messize_x = backsize_x + greysize_x
messize_y = greysize_y
grey = (128, 128, 128)
white = (255, 255, 255)
black = (0, 0, 0)

img = Image.new('RGB', (width*4, height*4), black)

back = Image.open('pic/70.gif') # size: 134*32
back = back.resize((134*4, 32*4))
back = back.transpose(Image.FLIP_LEFT_RIGHT)
background = Image.new('RGB', (messize_x, messize_y), black)
background.paste(back, (0, 0))
background.paste(back, (0, backsize_y))
background.paste(back, (0, backsize_y*2))
background.paste(back, (0, backsize_y*3))
draw_back = ImageDraw.Draw(background)
draw_back.rectangle((backsize_x, 0, backsize_x + greysize_x, greysize_y), outline=grey, fill=grey)
draw_back.rectangle((0, 0, backsize_x + greysize_x, greysize_y), outline=white, width=3)


draw = ImageDraw.Draw(img)

for mes in range(max_mes):
    # 画出背景
    # get x and y of mes
    column = mes//4
    row = 3-mes%4
    x = column * (backsize_x + greysize_x)
    y = row * (greysize_y)
    img.paste(background, (x, y))
    # 写小节名
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 60)
    font_x, font_y = font.getsize(str(mes+1))
    draw.text((x+backsize_x + greysize_x/2 - font_x/2, y+greysize_y/2 - font_y/2), str(mes+1), fill=white, font=font)
    # , y+greysize_y/2-10), str(mes+1), fill=white, font=font)

# 画长条
rail_x = {
        0: 0,
        1: 36,
        2: 49,
        3: 62,
        4: 75,
        5: 88,
        6: 101,
        7: 114
    }
for long_ in long: # 小节，轨道，长按开始位置，高度
    # 确定长条种类
    if long_[1] == 0: 
        if long_[4] == 0.5: note_img = Image.open('pic/ls.gif')
        if long_[4] == -0.5: note_img = Image.open('pic/hs.gif')
    if long_[1] == 1 or long_[1] == 3 or long_[1] == 5 or long_[1] == 7: 
        if long_[4] == 0.5: note_img = Image.open('pic/lw.gif')
        if long_[4] == -0.5: note_img = Image.open('pic/hw.gif')
    if long_[1] == 2 or long_[1] == 4 or long_[1] == 6: 
        if long_[4] == 0.5: note_img = Image.open('pic/lb.gif')
        if long_[4] == -0.5: note_img = Image.open('pic/hb.gif')
    
    note_img = note_img.resize([note_img.size[0]*4, (long_[3]+4)*4])

    column = long_[0]//4
    row = 3-long_[0]%4
    x = column * (backsize_x + greysize_x) + (rail_x[long_[1]] + long_[1])*4 # +rail 以居中
    y = row * (greysize_y) + (long_[2]-5)*4 # 储存时+4，所以要-4    

    img.paste(note_img, (x ,y))

for index, row in data.iterrows():
    
    # 画出notes
    for key_i in range(8):
        if row[key_i] == 1 or row[key_i] == -1:
            print("rail =" + str(key_i) + "mes =" + str(row[9]) + "note =" + str(row[key_i]) + "top =" + str(index))
            
            note_img, location = drawer(key_i, int(row[9]), row[key_i], index)
            img.paste(note_img, location)



# draw background
img.show()
img.save('test.png')
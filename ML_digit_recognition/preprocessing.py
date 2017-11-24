# -*-- coding = utf-8 --*-
from PIL import Image
import numpy as np
import os
import re
import pickle

height = 17
width = 10

def file_name(file_dir):
    ret = []
    for root, dirs, files in os.walk(file_dir):
        ret.extend(files)
    return ret

train_files = file_name('train')
test_files = file_name('test')

def convertimg(img_path):
    # Load a color image
    image = Image.open(img_path)

    # Convert to grey level image
    imgry = image.convert('L')

    # Setup a converting table with constant threshold
    threshold = 180
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    # convert to binary image by the table
    bim = imgry.point(table,"1")
    #bim.save('out.bmp')
    return bim

def get_crop_imgs(img):
    # split image into four child images
    child_img_list = []
    for i in range(4):
        x = 2+i * 14
        y = 6
        child_img = img.crop((x, y, x + width, y + height))
        child_img_list.append(cleanimg(child_img))
    return child_img_list

def get_feature(img):

    width, height = img.size

    pixel_cnt_list = []

    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

def convert_data():
    print("convert train data now")
    f = open('data/train_pix_feature_xy.txt', 'w')
    out = []
    for img_path in train_files:
        bim = convertimg('train/'+img_path)
        child_img_list = get_crop_imgs(bim)
        reg=re.findall('[0-9]+',img_path)[0]
        for i in range(4):
            f.write(reg[i])
            features = get_feature(child_img_list[i])
            for idx,idy in enumerate(features):
                f.write(' '+str(idx+1)+':'+str(idy))
            features.append(int(reg[i]))
            out.append(features)
            f.write('\n')

    output = open('data/train.pkl', 'wb')

    # Pickle dictionary using protocol 0.
    pickle.dump(np.array(out), output)
    output.close()
    f.close()

    print("convert test data now")

    f = open('data/test_pix_feature_xy.txt','w')
    out = []
    for img_path in test_files:
        bim = convertimg('test/'+img_path)
        child_img_list = get_crop_imgs(bim)
        reg=re.findall('[0-9]+', img_path)[0]
        for i in range(4):
            f.write(reg[i])
            features = get_feature(child_img_list[i])
            for idx,idy in enumerate(features):
                f.write(' '+str(idx+1)+':'+str(idy))
            features.append(int(reg[i]))
            out.append(features)
            f.write('\n')

    output = open('data/test.pkl', 'wb')

    # Pickle dictionary using protocol 0.
    pickle.dump(np.array(out), output)
    output.close()
    f.close()

def convert_input(file_path):
    inputfiles = file_name(file_path)
    idx = 0
    ret ={}
    ans = []
    for img_path in inputfiles:
        bim = convertimg(file_path+'/'+img_path)
        child_img_list = get_crop_imgs(bim)
        reg=re.findall('[0-9]+', img_path)[0]
        ans.append(reg)
        ret.setdefault(idx,[])
        for i in range(4):
            features = get_feature(child_img_list[i])
            ret[idx].append(features)
        idx+=1
    return ans,ret

def sum_9_region(img, x, y):
    cur_pixel = img.getpixel((x, y))
    width = img.width
    height = img.height

    if cur_pixel == 1:
        return 0

    dx = [1,1,1,0,0,0,-1,-1,-1]
    dy = [1,0,-1,1,0,-1,1,0,-1]

    s = 0
    for i,j in zip(dx,dy):
        if dx[i]+x>=0 and dx[i]+x<width and dy[j]+y>=0 and dy[j]+y<height:
            if img.getpixel((dx[i]+x,dy[j]+y))>0:
                tmp = 1
            else:
                tmp = 0
            s = s+tmp
    return 9-s

def cleanimg(img):
    width = img.width
    height = img.height

    for x in range(width):
        for y in range(height):
            if sum_9_region(img,x,y)<=3:
                img.putpixel((x, y), 1)
    return img

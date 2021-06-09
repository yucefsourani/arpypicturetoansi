#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# yucef sourni <youssef.m.sourani@gmail.com>
#
#
#
from PIL import Image
import os


character=["@","#","S","%","?","*","+",";",":",",","."]
#character=[".",".",".",".",".",".",".",".",".",".","."]

RESET="\033[0m"

    
def print_colored(image_location,
                  character=character,
                  keep_original_size=False,
                  width_r=60,
                  heigth_r=30,
                  convert_to_black=False,
                  aspectratio=False,
                  color_bg=False,
                  color_fb_and_bb=True,
                  end="\n"):
                      
    if len(character)<11:
        character += (11 - len(character)) * "."
    img = Image.open(image_location)
    width,heigth = img.size
    if keep_original_size:
        if aspectratio:
            aspect_ratio = heigth / width
            heigth = aspect_ratio * width
            img    = img.resize( (width , int(heigth)) )
    else:
        if aspectratio:
            aspect_ratio = heigth_r / width_r
            heigth_r = aspect_ratio * width_r
        img    = img.resize( (width_r , int(heigth_r)) )
        width  = width_r
        heigth = heigth_r
    
    colored_pixel = img.getdata()
    
    final_image = ""
    count       = 1
    for index in range( 0 , len(colored_pixel) ):
        c_index = colored_pixel[index]
        if isinstance(c_index,int):
            c_index = (c_index,c_index,c_index)
        else:
            if convert_to_black:
                img = img.convert('L')
                colored_pixel=img.getdata()
                c_index = colored_pixel[index]
                c_index = (c_index,c_index,c_index)
                
        len_rgb = len(c_index)
        if len_rgb > 3:
            r,g,b = c_index[0:-1]
        else:
            r,g,b = c_index
        if color_fb_and_bb:
            final_image +=  "\033[38;2;{};{};{}m\033[48;2;{};{};{}m{}{}".format(r,g,b,r,g,b,character[sum(c_index)//(len_rgb*25)],RESET)
        elif color_bg:
            final_image +=  "\033[48;2;{};{};{}m{}{}".format(r,g,b,character[sum(c_index)//(len_rgb*25)],RESET)
        else:
            final_image +=  "\033[38;2;{};{};{}m{}{}".format(r,g,b,character[sum(c_index)//(len_rgb*25)],RESET)
        if count == width:
            final_image += end
            count = 0
        count += 1
    print(final_image)
    return final_image

def save_colored_to_file(file_location,
                         image_location,
                         override_file=False,
                         character=character,
                         keep_original_size=False,
                         width_r=60,
                         heigth_r=30,
                         convert_to_black=False,
                         aspectratio=False,
                         color_bg=False,
                         color_fb_and_bb=True,
                         end="\n"):
                             
    text = print_colored(image_location,
                         character,
                         keep_original_size,
                         width_r,
                         heigth_r,
                         convert_to_black,
                         aspectratio,
                         color_bg,
                         color_fb_and_bb,
                         end)
    if text :
        if os.path.exists(file_location):
            if override_file:
                try :
                    with open(file_location,"w") as mf:
                        mf.write(text)
                except Exception as err:
                    print("{}".format(err))
                    return False
            else:
                return False
        else:
            try :
                with open(file_location,"w") as mf:
                    mf.write(text)
            except Exception as err:
                print("{}".format(err))
                return False
    else:
        return False
    return True

if __name__ == "__main__":
    image_l = "pf.jpg"
    print(save_colored_to_file("2.text",image_l,color_fb_and_bb=False))
    print(save_colored_to_file("2.text",image_l,character="#"*11,color_fb_and_bb=False))
    print(save_colored_to_file("2.text",image_l,character="#"*11,override_file=True))
    
    image_l2 = "Flag_of_the_Lebanese_Republic.png"
    print(save_colored_to_file("3.text",image_l2,color_fb_and_bb=False))
    print(save_colored_to_file("3.text",image_l2,character="#"*11,color_fb_and_bb=False))
    print(save_colored_to_file("3.text",image_l2,character="#"*11,override_file=True))

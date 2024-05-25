from PIL import Image
import rsa
import os
from utils import ALPHA_LEVEL   # alpha value to ignore pixel

def get_two_bit_data(img, data_len, two_bit_data):
    n = 0
    for row_idx in range(img.height):
        for column_idx in range(img.width):
            pixel = img.getpixel((column_idx, row_idx))[:3]
            for color in pixel:
                if n < 48:
                    n += 1
                else:
                    two_bit = color & 0b00000011
                    two_bit_data.append(two_bit)
                    n += 1
                    if n > data_len+48:
                        return 
                    
def get_two_bit_data2(img, data_len, two_bit_data):
    n = 0
    four_channel = len(img.getpixel((0, 0))) == 4
    for row_idx in range(img.height):
        for column_idx in range(img.width):
            pixel = img.getpixel((column_idx, row_idx))
            if four_channel and pixel[3] < ALPHA_LEVEL:
                continue
            for color in pixel[:3]:
                if n < 48:
                    n += 1
                else:
                    two_bit = color & 0b00000011
                    two_bit_data.append(two_bit)
                    n += 1
                    if n > data_len+48:
                        return
            
                    
def get_file_ext(img):
    n = 0
    two_bit_ext = []
    file_ext = []
    for row_idx in range(img.height):
        for column_idx in range(img.width):
            pixel = img.getpixel((column_idx, row_idx))
            if pixel[3] < ALPHA_LEVEL:
                continue
            for color in pixel[:3]:
                two_bit = color & 0b11
                if n < 32:
                    two_bit_ext.append(two_bit)
                    n += 1
                else:
                    for i in range(0, 32, 4):
                        byte = two_bit_ext[i] << 6 | two_bit_ext[i+1] << 4 | two_bit_ext[i+2] << 2 | two_bit_ext[i+3]
                        file_ext.append(byte)
                        if byte == 0:
                            return "."+ "".join(chr(i) for i in file_ext[:-1])
                    return "."+ "".join(chr(i) for i in file_ext)
    

def get_data_length(img):
    n = 0
    len_data = []
    data_len = 0
    for row_idx in range(img.height):
        for column_idx in range(img.width):
            pixel = img.getpixel((column_idx, row_idx))
            if pixel[3] < ALPHA_LEVEL:
                continue
            for color in pixel[:3]:
                two_bit = color & 0b11
                if n < 32:
                    n += 1
                elif n < 48:
                    len_data.append(two_bit)
                    n += 1
                else:
                    for i in range(30, -1, -2):
                        data_len += len_data[(30-i)//2] << i
                    return data_len
                        

def get_data(two_bit_data, data):
    for i in range(0, len(two_bit_data[:-4]), 4):
        p1 = two_bit_data[i] << 6
        p2 = two_bit_data[i+1] << 4
        p3 = two_bit_data[i+2] << 2
        p4 = two_bit_data[i+3]
        data.append(p1 | p2 | p3 | p4)

def max_data_size_for_enc(key):
    return rsa.common.bit_size(key.n) // 8 - 11

# check if data can be decrypted with given key
def can_enc(data, key):
    return len(data) <= max_data_size_for_enc(key)

def decrypt_data(data, key):
    return rsa.decrypt(data, key)

def create_output_file(data, output_path):
    with open(output_path, "wb") as file:
        file.write(data)

def extract(image_path, output_path, key=""):
    img = Image.open(image_path)
    file_ext = get_file_ext(img)
    data_len = get_data_length(img)
    two_bit_data = []
    get_two_bit_data2(img, data_len, two_bit_data)
    data = []
    get_data(two_bit_data, data)
    data = bytes([i for i in data])
    if key != "":
        if hasattr(key, 'n') and hasattr(key, 'e'):
            data = decrypt_data(data, key)
        else:
            print("Invalid key")
            return
    create_output_file(data, output_path+file_ext)

"""
def extract(image_path, output_path, private_key):
    img = Image.open(image_path)
    two_bit_data = []
    data_len = get_data_length(img)
    get_two_bit_data(img, data_len, two_bit_data)
    data = []
    get_data(two_bit_data, data)
    decrypted_data = decrypt_data(data, private_key)
    create_output_file(decrypted_data, output_path)
"""
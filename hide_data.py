from PIL import Image
import os
import rsa
import utils
from utils import ALPHA_LEVEL

PUBLIC = "RSAPublic"
AES = "AES"

TOO_LARGE_DATA = "tld"
INVALID_KEY = "ik"

def get_file_content(file_path):
    with open(file_path, "rb") as f:
        return f.read()
    
# split each byte of data into 2-bit 4 pieces and append to list
def get_two_bit_data(file_content, two_bit_data):
    for char in file_content:
        two_bit_data.append(char >> 6)
        two_bit_data.append((char >> 4) & 0b11)
        two_bit_data.append((char >> 2) & 0b11)
        two_bit_data.append(char & 0b11)

def get_file_ext(file_path):
    return os.path.splitext(file_path)[1][1:]

# 8 bytes (64 bits): 32 2-bit pieces for file extension
def add_ext_to_two_bit_data(file_ext, two_bit_data):
    two_bit_ext = []
    for char in file_ext:
        char = ord(char)
        two_bit_ext.append(char >> 6)
        two_bit_ext.append((char >> 4) & 0b11)
        two_bit_ext.append((char >> 2) & 0b11)
        two_bit_ext.append(char & 0b11)
    for _ in range(32 - len(two_bit_ext)):
        two_bit_ext.append(0)
    return two_bit_ext + two_bit_data

# append length of the two bit data to the head of the list
# length data is 32 bit, 16 2-bit  pieces
def add_len_to_two_bit_data(two_bit_data):
    two_bit_data_len = len(two_bit_data)
    len_data = []
    chooser = 0xC0000000
    for shift in range(30, -1, -2):
        len_data.append((two_bit_data_len & chooser) >> shift)
        chooser = chooser >> 2
    return len_data + two_bit_data

# modify image by hiding data into it
def modify_image(img, two_bit_data):
    column_count = img.size[0]
    for idx, two_bit in enumerate(two_bit_data):
        row_idx = int(idx / (column_count * 3))
        idx = idx % (column_count * 3)
        column_idx = int(idx / 3)
        idx = idx % 3
        pixel = list(img.getpixel((column_idx, row_idx)))
        pixel[idx] = (pixel[idx] & 0b11111100) | two_bit
        img.putpixel((column_idx, row_idx), tuple(pixel))
    
def modify_image2(img, two_bit_data):
    i = 0   #index for two bit data
    len_data = len(two_bit_data)
    four_channel = len(img.getpixel((0, 0))) == 4
    for row_idx in range(img.height):
        for column_idx in range(img.width):
            pixel = list(img.getpixel((column_idx, row_idx)))
            if four_channel and pixel[3] < ALPHA_LEVEL:
                continue
            for colord_idx in (0, 1, 2):
                color = pixel[colord_idx]
                color = (color & 0b11111100) | two_bit_data[i]
                pixel[colord_idx] = color
                i += 1
                if i >= len_data:
                    img.putpixel((column_idx, row_idx), tuple(pixel))
                    return
            img.putpixel((column_idx, row_idx), tuple(pixel))
            

def max_data_size_for_enc(key):
    return rsa.common.bit_size(key.n) // 8 - 11

# check if data can be encrypted with given key
def can_enc(data, key):
    return len(data) <= max_data_size_for_enc(key)

def encrypt_data(data, key):
    # data must be in byte format
    return rsa.encrypt(data, key)

def max_data_size(img):
    total = int((img.size[0] * img.size[1] * 3 - 16 - 32)/4)
    if len(img.getpixel((0, 0))) == 3:
        return total
    else:
        width, height = img.size
        for row_idx in range(height):
            for column_idx in range(width):
                pixel = img.getpixel((column_idx, row_idx))
                if pixel[3] < ALPHA_LEVEL:
                    total -= 1
    return total
            

def hide(image_path, file_path, output_path, key="", enc_type=""):
    img = Image.open(image_path)
    max_size = max_data_size(img)
    file_content = get_file_content(file_path)
    if (max_size < len(file_content)):
        return TOO_LARGE_DATA
    if key != "":
        if hasattr(key, 'n') and hasattr(key, 'e'):
            file_content = encrypt_data(file_content, key)
        else:
            return INVALID_KEY
    two_bit_data = []
    get_two_bit_data(file_content, two_bit_data)
    two_bit_data = add_len_to_two_bit_data(two_bit_data)
    two_bit_data = add_ext_to_two_bit_data(get_file_ext(file_path), two_bit_data)
    modify_image2(img, two_bit_data)
    img.save(output_path)



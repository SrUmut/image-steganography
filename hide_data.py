# Default modules
import os

# Modules that need to be downloaded
import rsa
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ALPHA_LEVEL = 128

ENC_ERR = "Encryption Error"
NES = "Not Enough Space"
DONE = "Successfuly Done"

def get_file_content(file_path):
    with open(file_path, "rb") as f:
        return f.read()
    
def get_file_extension(file_path):
    return os.path.splitext(file_path)[1][1:]

def content_to_two_bit_data(file_content, two_bit_data):
    for char in file_content:
        two_bit_data.append(char >> 6)
        two_bit_data.append((char >> 4) & 0b11)
        two_bit_data.append((char >> 2) & 0b11)
        two_bit_data.append(char & 0b11)

def get_len_data(two_bit_data):
    len_data = [int(byte) for byte in len(two_bit_data).to_bytes(4, byteorder="big")]
    for _ in range(4 - len(len_data)):
        len_data.insert(0, 0)
    return len_data

def get_ext_data(file_ext):
    ext_data = [ord(character) for character in file_ext]
    for _ in range(8 - len(ext_data)):
        ext_data.append(0)
    return ext_data

def encrypt_metadata(ext_data, len_data):
    byte_data = bytes(ext_data+len_data)
    key = b'i\x8d\x1eJ\xd1^Z\x7f\xf8\xb3K\x93\x94\xc6\xf0\xcf'
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_metadata = cipher.encrypt(pad(byte_data, AES.block_size))
    return encrypted_metadata

def get_two_bit_metadata(encrypted_metadata):
    two_bit_list = []
    for byte in encrypted_metadata:
        two_bit_list.append(byte >> 6)
        two_bit_list.append((byte >> 4) & 0b11)
        two_bit_list.append((byte >> 2) & 0b11)
        two_bit_list.append(byte & 0b11)
    return two_bit_list

# 4 bytes = 32 bits = 16 2-bit pieces to hide data length
def append_len(two_bit_data):
    length = len(two_bit_data)
    len_data = []
    chooser = 0xC0000000
    for shift in range(30, -1, -2):
        len_data.append((length & chooser) >> shift)
        chooser = chooser >> 2
    return len_data + two_bit_data

# 8 bytes = 64 bits = 32 2-bit pieces to hide file extension
def append_ext(file_ext, two_bit_data):
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

def modify_image(img, two_bit_data):
    i = 0 # index for two_bit_data
    len_data = len(two_bit_data)
    # is image four channel (rgba) or not (rgb)
    four_channel = len(img.getpixel((0, 0))) == 4 
    for row_idx in range(img.height):
        for column_idx in range(img.width):
            pixel = list(img.getpixel((column_idx, row_idx)))
            # if alpha channel is less than minimum value skip that pixel
            if four_channel and pixel[3] < ALPHA_LEVEL:
                continue
            # iterate over color channels of pixel and hide data to each channel
            for color_idx in (0, 1, 2):
                color = pixel[color_idx]
                color = (color & 0b11111100) | two_bit_data[i]
                pixel[color_idx] = color
                i += 1
                if i >= len_data:
                    img.putpixel((column_idx, row_idx), tuple(pixel))
                    return True
            img.putpixel((column_idx, row_idx), tuple(pixel))
    # If code comes here it means there is no eanough space for the data in the image
    return False



def main(image_path, file_path, output_path, key):
    img = Image.open(image_path)
    file_content = get_file_content(file_path)
    if key:
        try:
            file_content = rsa.encrypt(file_content, key)
        except:
            return ENC_ERR
    two_bit_data = []
    content_to_two_bit_data(file_content, two_bit_data)
    #two_bit_data = append_len(two_bit_data)
    file_ext = get_file_extension(file_path)
    #two_bit_data = append_ext(file_ext, two_bit_data)
    len_data = get_len_data(two_bit_data)
    ext_data = get_ext_data(file_ext)
    metadata = encrypt_metadata(ext_data, len_data)
    two_bit_metadata = get_two_bit_metadata(metadata)
    two_bit_data = two_bit_metadata + two_bit_data
    done = modify_image(img, two_bit_data)
    if not done:
        return NES
    img.save(output_path)
    return DONE



# Modules that need to be downloaded
from PIL import Image
import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# My modules
from hide_data import ALPHA_LEVEL

def get_enc_metadata(img):
    n = 0
    two_bit_metadata = []
    meta_data = []
    # is image four channel (rgba) or not (rgb)
    four_channel = len(img.getpixel((0, 0))) == 4 
    for row_idx in range(img.height):
        for column_idx in range(img.width):
            pixel = img.getpixel((column_idx, row_idx))
            if four_channel and pixel[3] < ALPHA_LEVEL:
                continue
            for color in pixel[:3]:
                two_bit = color & 0b11
                if n < 64:
                    two_bit_metadata.append(two_bit)
                    n += 1
                else:
                    for i in range(0, 64, 4):
                        meta_data.append(two_bit_metadata[i] << 6 | two_bit_metadata[i+1] << 4 | two_bit_metadata[i+2] << 2 | two_bit_metadata[i+3])
                    return bytes(meta_data)

def get_ext_and_data_len(enc_metadata):
    key = b'i\x8d\x1eJ\xd1^Z\x7f\xf8\xb3K\x93\x94\xc6\xf0\xcf'
    cipher = AES.new(key, AES.MODE_ECB)
    dec_metadata = unpad(cipher.decrypt(enc_metadata), AES.block_size)
    file_ext = ["."]
    for byte in dec_metadata[:8]:
        if byte == 0:
            break
        file_ext.append(chr(byte))
    file_ext = "".join(file_ext)
    length = int.from_bytes(bytes=dec_metadata[8:], byteorder="big")
    return (file_ext, length)
                
def get_two_bit_data(img, data_len, two_bit_data):
    n = 0
    # is image four channel (rgba) or not (rgb)
    four_channel = len(img.getpixel((0, 0))) == 4 
    for row_idx in range(img.height):
        for column_idx in range(img.width):
            pixel = img.getpixel((column_idx, row_idx))
            if four_channel and pixel[3] < ALPHA_LEVEL:
                continue
            for color in pixel[:3]:
                if n < 64:
                    n += 1
                else:
                    two_bit = color & 0b11
                    two_bit_data.append(two_bit)
                    n += 1
                    if n >= data_len + 64:
                        return
                    
def get_data(two_bit_data, data):
    for i in range(0, len(two_bit_data), 4):
        quarter1 = two_bit_data[i] << 6
        quarter2 = two_bit_data[i+1] << 4
        quarter3 = two_bit_data[i+2] << 2
        quarter4 = two_bit_data[i+3]
        data.append(quarter1 | quarter2 | quarter3 | quarter4)
    return bytes(data)

def save_output(data, output_path):
    with open(output_path, "wb") as f:
        f.write(data)

def main(image_path, output_path, key):
    img = Image.open(image_path)
    enc_metadata = get_enc_metadata(img)
    file_ext, data_len = get_ext_and_data_len(enc_metadata)
    two_bit_data = []
    get_two_bit_data(img, data_len, two_bit_data)
    data = []
    data = get_data(two_bit_data, data)
    if key:
        data = rsa.decrypt(data, key)
    save_output(data, output_path+file_ext)
    return True


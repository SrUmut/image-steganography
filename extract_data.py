from PIL import Image


def get_two_bit_data(img, two_bit_data):
    n = 0
    for row_idx in range(img.height):
        for column_idx in range(img.width):
            pixel = img.getpixel((column_idx, row_idx))[:3]
            for color in pixel:
                two_bit = color & 0b00000011
                two_bit_data.append(two_bit)
                n += 1
                if ((n % 4 == 0) and (two_bit == 0) and (two_bit_data[-2] == 0) and (two_bit_data[-3] == 0) and (two_bit_data[-4] == 0)):
                    return

def get_data(two_bit_data, data):
    for i in range(0, len(two_bit_data[:-4]), 4):
        p1 = two_bit_data[i] << 6
        p2 = two_bit_data[i+1] << 4
        p3 = two_bit_data[i+2] << 2
        p4 = two_bit_data[i+3]
        data.append(p1 | p2 | p3 | p4)

def create_output_file(data, output_path):
    with open(output_path, "wb") as file:
        file.write(b"".join([bytes([i]) for i in data]))

def main(image_path, output_path):
    img = Image.open(image_path)
    two_bit_data = []
    get_two_bit_data(img, two_bit_data)
    data = []
    get_data(two_bit_data, data)
    create_output_file(data, output_path)

    
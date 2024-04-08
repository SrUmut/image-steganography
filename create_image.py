from PIL import Image

def get_file_content(file_path):
    with open(file_path, "rb") as f:
        return f.read()
    
def get_two_bit_data(file_content, two_bit_data, image):
    if (len(file_content)+1) * 4 > image.width * image.height * 3:
        raise Exception("Data file is too large to fit in the image.")
    for char in file_content:
        #char = ord(char)
        two_bit_data.append(char >> 6)
        two_bit_data.append((char >> 4) & 0b0011)
        two_bit_data.append((char >> 2) & 0b000011)
        two_bit_data.append(char & 0b00000011)

    # add EOF (0b00000000) to the end of the data
    for _ in range(4):
        two_bit_data.append(0)

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

def main(image_path, file_path, output_path):
    img = Image.open(image_path)
    file_content = get_file_content(file_path)
    two_bit_data = []
    get_two_bit_data(file_content, two_bit_data, img)
    modify_image(img, two_bit_data)
    img.save(output_path)

This is a simple python script to hide data inside image.

### Quick Start:
* pip install -r requirements.txt
* python main.py
* Provide necessary paths

### How It Works:
#### Hiding data:
It takes the data and split every character(8 bits) to 4, every part is 2 bit. Then the leasts 2 significant bit of colors (RGB) in png is changed to these splitted bits of data by order and then save the output image. It also hides the length of the data and the data file's extension at the beginning of the image.

#### Extracting data:
Read the length of the data (n) and the file extension from the beginning of the image. Then read the next n 2-bits to create the data. Then concatanate every 4 2-bit group as a byte and save it.
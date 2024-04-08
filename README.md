This is a simple python script to hide data inside image.

### Quick Start:
* python main.py
* Enter 1 to hide data(.txt) inside image(.png), 2 to extract data from steganographic image
* Provide necessary paths

### How It Works:
#### Hiding data:
It takes the data and split every character(8 bits) to 4, every part is 2 bit. Then the leasts 2 significant bit of colors (RGB) in png is changed to these splitted bits by order and then save the new image.
#### Extracting data:
Read least 2 significant for every color until see the 4 bits that are 00. Then concatanate every 4 2-bit group as a byte and save it to a text file.
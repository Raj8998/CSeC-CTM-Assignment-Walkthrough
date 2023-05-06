#!/usr/bin/python3

import binascii

with open('image.jpg', 'wb') as image_file:
    image_file.write(binascii.a2b_hex(open('hexFile.txt', 'r').read().strip().replace(' ', '').replace('\n', '')))
# -*- coding: utf-8 -*-
from PIL import Image
import pytesseract
import sys

image = Image.open(sys.argv[1])
image.load()

imgry = image.convert('L')

print pytesseract.image_to_string(imgry)


















# vim: set ts=4 sw=4 sts=4 tw=100 et:

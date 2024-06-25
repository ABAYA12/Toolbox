from PyPDF2 import PdfMerger, PdfReader
from PIL import Image
import cv2
import numpy as np
import pdf2image

def merge_pdfs(files, output):
    merger = PdfMerger()
    for file in files:
        merger.append(PdfReader(file))
    merger.write(output)
    merger.close()

def remove_image_background(image, output):
    img = Image.open(image).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:  # finding white color by its RGB value
            new_data.append((255, 255, 255, 0))  # making white color transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output)

def convert_to_grayscale(image, output):
    img = Image.open(image).convert('L')
    img.save(output)

def resize_image(image, width, height, output):
    img = Image.open(image)
    img = img.resize((width, height))
    img.save(output)

def pdf_to_images(pdf, output_dir):
    images = pdf2image.convert_from_path(pdf)
    for i, img in enumerate(images):
        img.save(f"{output_dir}/page_{i + 1}.png", "PNG")

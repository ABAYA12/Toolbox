from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app.utils import merge_pdfs, remove_image_background, convert_to_grayscale, resize_image, pdf_to_images
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/merge_pdfs', methods=['GET', 'POST'])
def merge_pdfs_view():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        output_path = os.path.join('uploads', 'merged.pdf')
        merge_pdfs([file for file in files], output_path)
        return send_file(output_path, as_attachment=True)
    return render_template('merge_pdfs.html')

@main.route('/remove_bg', methods=['GET', 'POST'])
def remove_bg_view():
    if request.method == 'POST':
        image = request.files['image']
        output_path = os.path.join('uploads', 'no_bg.png')
        remove_image_background(image, output_path)
        return send_file(output_path, as_attachment=True)
    return render_template('remove_bg.html')

@main.route('/grayscale', methods=['GET', 'POST'])
def grayscale_view():
    if request.method == 'POST':
        image = request.files['image']
        output_path = os.path.join('uploads', 'grayscale.png')
        convert_to_grayscale(image, output_path)
        return send_file(output_path, as_attachment=True)
    return render_template('grayscale.html')

@main.route('/resize_image', methods=['GET', 'POST'])
def resize_image_view():
    if request.method == 'POST':
        image = request.files['image']
        width = int(request.form['width'])
        height = int(request.form['height'])
        output_path = os.path.join('uploads', 'resized.png')
        resize_image(image, width, height, output_path)
        return send_file(output_path, as_attachment=True)
    return render_template('resize_image.html')

@main.route('/pdf_to_image', methods=['GET', 'POST'])
def pdf_to_image_view():
    if request.method == 'POST':
        pdf = request.files['pdf']
        output_dir = os.path.join('uploads', 'pdf_images')
        os.makedirs(output_dir, exist_ok=True)
        pdf_to_images(pdf, output_dir)
        files = os.listdir(output_dir)
        file_paths = [os.path.join(output_dir, file) for file in files]
        return send_file(file_paths[0], as_attachment=True)  # send the first image as example
    return render_template('pdf_to_image.html')

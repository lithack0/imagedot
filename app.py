import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image

app = Flask(__name__)

# Create an "uploads" folder if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Save the uploaded image to the "uploads" folder
        file.save(os.path.join('uploads', 'uploaded_image.png'))
        
        # Process the uploaded image (your existing code)
        image_path = 'uploads/uploaded_image.png'
        image = Image.open(image_path)
        binary_data = image.tobytes()
        width, height = 640, 480
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        data_index = 0
        ind1 = []
        ind0 = []
        for y in range(height):
            for x in range(width):
                if data_index < len(binary_data):
                    binary_value = int(binary_data[data_index])
                    data_index += 1
                    if binary_value == 1:
                        pixels[x, y] = (255, 255, 255)
                        ind1.append(data_index - 1)
                    else:
                        pixels[x, y] = (0, 0, 0)
                        ind0.append(data_index - 1)
                else:
                    pixels[x, y] = (0, 0, 0)
        image.save(os.path.join('uploads', 'generated_image.png'))

        return redirect(url_for('show_generated_image'))

@app.route('/show_generated_image')
def show_generated_image():
    return send_file(os.path.join('uploads', 'generated_image.png'))

if __name__ == '__main__':
    app.run(debug=True)

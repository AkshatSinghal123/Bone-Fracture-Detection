import os
from flask import Flask, request, jsonify, send_file
from tkinter import filedialog
import customtkinter as ctk
import pyautogui
import pygetwindow
from PIL import ImageTk, Image
from predictions import predict

app = Flask(__name__)

project_folder = os.path.dirname(os.path.abspath(__file__))
folder_path = project_folder + '/images/'

filename = ""

@app.route('/upload_image', methods=['POST'])
def upload_image():
    global filename
    f_types = [("All Files", "*.*")]
    filename = filedialog.askopenfilename(filetypes=f_types, initialdir=project_folder+'/test/Wrist/')
    img = Image.open(filename)
    img_resized = img.resize((int(256 / img.height * img.width), 256))  # new width & height
    img = ImageTk.PhotoImage(img_resized)
    return jsonify({'message': 'Image uploaded successfully'})

@app.route('/predict', methods=['GET'])
def predict_image():
    global filename
    if filename == "":
        return jsonify({'error': 'Please upload an image first'})
    bone_type_result = predict(filename)
    result = predict(filename, bone_type_result)
    if result == 'fractured':
        prediction_result = {'result': 'Fractured', 'bone_type': bone_type_result}
    else:
        prediction_result = {'result': 'Normal', 'bone_type': bone_type_result}
    return jsonify(prediction_result)

@app.route('/save_result', methods=['GET'])
def save_result():
    tempdir = filedialog.asksaveasfilename(parent=self, initialdir=project_folder + '/PredictResults/',
                                           title='Please select a directory and filename', defaultextension=".png")
    screenshots_dir = tempdir
    window = pygetwindow.getWindowsWithTitle('Bone Fracture Detection')[0]
    left, top = window.topleft
    right, bottom = window.bottomright
    pyautogui.screenshot(screenshots_dir)
    im = Image.open(screenshots_dir)
    im = im.crop((left + 10, top + 35, right - 10, bottom - 10))
    im.save(screenshots_dir)
    return jsonify({'message': 'Result saved successfully'})

if __name__ == "__main__":
    app.run(debug=True)

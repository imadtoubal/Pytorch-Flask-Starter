from flask import Flask, render_template, request
from models import MobileNet
import os 

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

model = MobileNet()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/infer', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        saveLocation = f.filename
        f.save(saveLocation)
        inference = model.infer(saveLocation)
        os.remove(saveLocation)
        return render_template('inference.html', name = inference)  
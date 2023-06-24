import os
from flask import Flask,request,render_template,jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
from chatmanager import ChatManager

UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)
CORS (app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
chatmanager = ChatManager()

#ルーティング
@app.route('/demo',methods=['POST','GET'])
def demo():
    if request.method == 'POST':  
        #postから受け取る
        prompt_string = request.form["prompt"]
        result_string = chatmanager.chat(prompt_string)

        return jsonify({"chat_response":result_string})
    else:
        return render_template('demo.html')
@app.route('/finetuning',methods=['POST','GET'])
def upload():
    print(request)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        fine_tuning_id = chatmanager.finetuning(filepath)
        return jsonify({"fine_tuning_id":fine_tuning_id})
    else:
        return render_template('finetuning.html')
@app.route('/finetuning_list',methods=['POST','GET'])
def get_finetuning_status():
    chatmanager.get_finetuning_list()
@app.route('/')
def index():
    return render_template('demo.html')

app.run(port=8000, debug=True)
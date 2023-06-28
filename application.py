import os

from flask import Flask,render_template,request,jsonify, flash, redirect
from flask_cors import CORS
from werkzeug.utils import secure_filename
from chatmanager import ChatManager

UPLOAD_FOLDER = './uploads/'
chatmanager = ChatManager()
def show_demo():
    return render_template("demo.html")

def post_test():
    if request.method == 'POST':  
        #receive from post
        prompt_string = request.form["prompt"]
        result_string = chatmanager.chat(prompt_string)
        return jsonify({"chat_response":result_string})
    else:
        print("GET")
        return render_template('demo.html')
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        fine_tuning_id = chatmanager.finetuning(filepath)
        return jsonify({"fine_tuning_id":fine_tuning_id})
    else:
        return render_template('finetuning.html')
def get_finetuning_status():
   finetune_status = chatmanager.get_finetuning_list()
   return finetune_status

def post_example():
    return "POST request successful!"
# EB looks for an 'application' callable by default.
application = Flask(__name__)
#set CORS
CORS (application)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: show_demo()))

application.add_url_rule('/demo', 'post_demo', post_test, methods=['POST','GET'])
application.add_url_rule('/finetuning', 'finetuning_demo', upload, methods=['POST','GET'])
application.add_url_rule('/post_example', 'post_example', post_example, methods=['POST'])
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
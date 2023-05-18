from flask import Flask,request,render_template,jsonify
from chatmanager import ChatManager

app = Flask(__name__)
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

@app.route('/')
def index():
    return render_template('demo.html')

app.run(port=8000, debug=True)
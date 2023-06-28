import openai

#KEY
KEY = ''
openai.api_key = KEY

class ChatManager:
    #init
    def __init__(self) :
        self.model = 'gpt-3.5-turbo'
        self.messages = [{'role': 'system', 'content': 'you are agent'}]
        self.params = {}
        self.setup_params()
    #set message
    def compose_message(self, role, content):
        self.messages.append({'role':role, 'content':content})
    #パラメータを設定
    def setup_params(self):
        self.params['model'] = self.model
        self.params['messages'] = self.messages
    #ChatCompletionを呼び出す
    def call_chat_api(self):
        completion = openai.ChatCompletion.create(**self.params)
        result = completion['choices'][0]['message']
        return result
    #ChatCompletionの結果を蓄積
    def get_response_from_api(self):
        result = self.call_chat_api()
        self.compose_message(result.role, result.content)
        #新しく取得したメッセージをレスポンスする
        return result
    #チャットをする
    def chat(self,prompt):
        self.compose_message('user',prompt)
        result = self.get_response_from_api()
        return result.content
    #finetuningを行う
    def finetuning(self,filename):
        upload_response = openai.File.create(
            file = open (filename,'rb'),
            purpose='fine-tune'
        )
        fine_tuning_response = openai.FineTune.create(
            model = 'davinci',
            training_file = upload_response.id
        )
        return fine_tuning_response['id']
    #finetuning状況チェック
    def get_finetuning_list(self,finetuning_id):
        fine_tune = openai.FineTune.retrive(finetuning_id)
        if 'status' not in fine_tune:
            print(f"Error: {fine_tune}")
            return None
        return fine_tune

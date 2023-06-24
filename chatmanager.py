import openai
#↓KEYを発行して更新をお願いします。
KEY = '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'
openai.api_key = KEY

class ChatManager:
    #初期処理
    def __init__(self) :
        self.model = 'gpt-3.5-turbo'
        self.messages = [{'role': 'system', 'content': 'あなたは旅行に詳しいです。'}]
        self.params = {}
        self.setup_params()
    #メッセージを設定
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
        print(filename)
        upload_response = openai.File.create(
            file = open (filename,'rb'),
            purpose='fine-tune'
        )
        print (upload_response)
        fine_tuning_response = openai.FineTune.create(
            model = 'davinci',
            training_file = upload_response.id
        )
        print(fine_tuning_response)
        return fine_tuning_response['id']
    #finetuning状況チェック
    def get_finetuning_list(self,finetuning_id):
        fine_tune = openai.FineTune.retrive(finetuning_id)
        if 'status' not in fine_tune:
            print(f"Error: {fine_tune}")
            return None
        return fine_tune['status'], fine_tune.get('fine_tuned_model', None)

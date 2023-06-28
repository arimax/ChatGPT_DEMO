function addMessage (prompt,response) {
    //レスポンスと質問を追加
    let new_div = document.createElement('div');
    let new_prompt = document.createElement('p');
    new_prompt.textContent = prompt;
    let new_response = document.createElement('p');
    new_response.textContent = response;

    new_div.appendChild(new_prompt);
    new_div.appendChild(new_response);

    let chat_history = document.getElementById('chat_history');
    chat_history.appendChild(new_div);
}
function chat() {
    const prompt = document.getElementById('prompt');
    let params = new URLSearchParams();
    params.append('prompt', prompt.value);
    console.log('POST'+ params);
    fetch('http://chatgpt-demo-202306241241-env.eba-ecdhhqj6.ap-northeast-1.elasticbeanstalk.com/demo',{
        method: 'POST',
        body: params,
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Success',data);
        addMessage (prompt.value,data['chat_response'])
    })
    .catch((error) => {
        console.log('error:',error);
    })
}

function uploadFineTuning() {
    if (document.getElementById("fine_tuing_upload").files == null) {
        return;
    }
    const file = document.getElementById("fine_tuing_upload").files[0];
    console.log("upload finetuning file")
    let formData = new FormData();
    formData.append('file',file);

    const url = 'http://chatgpt-demo-202306241241-env.eba-ecdhhqj6.ap-northeast-1.elasticbeanstalk.com/finetuning'

    const promise = fetch(url,{method: 'POST',body: formData});
    promise.then(response => {
        if (response.status != 200) {
            throw `response.status = ${response.status}, response.statusText = ${response.statusText}`;
        }
    })
    .then(jsondata => {
        console.log("Result is : " +jsondata)
    }).catch(err => {
        console.log("Error :"+ err)
    })
}

function getFinetuningStatus() {
    console.log("getFinetuningStatus")
    const params = new URLSearchParams();
    const tuningId = document.getElementById('tuning_id');
    console.log(tuningId)
    params.append('tuning_id', tuningId.value);
    fetch('http://localhost:8000/finetuning_status',{
        method: 'GET',
        body: params,
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Success',data);
    })
    .catch((error) => {
        console.log('error:',error);
    })
}
$(document).ready(function(){
    $('form input').change(function () {
      $('form p').text(this.files.length + " файл(-а) выбрано");
    });
});


function uploadFile(){
  let file = document.getElementById("upload-input").files[0];
  if (!file){
    alert("Нужно загрузить файл!");
  }else{
    let modal = $(".modal")
    modal.modal("show");

    let data = new FormData();
    data.append("file", file)

    fetch("upload_file", {
      method: "POST",
      body: data,
      contentType: 'application/json',
      headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": $.cookie("csrftoken")
      },
    }).then(function (response) {
      response.json().then(
          function (data) {
              refreshFileInput();
              if (data["response"]) {
                let option  = {
                  animation: true,
                  delay: 5000
                }
                const myToast = document.getElementById('doneToast');
                let bsToast = new bootstrap.Toast(myToast, option);
                bsToast.show();
              }else{
                
              }
          }
      )
    })
  }
}

function logout(){
  fetch("logout", {
    method: "POST",
    contentType: 'application/json',
    headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": $.cookie("csrftoken")
    },
  }).then(function (response) {
    response.json().then(
        function (data) {
            if (data["response"]) {
                window.location.replace("distributor");
            }
        }
    )
  })
}

function closeToast(id){
  $(`#${id}`).toast("hide");
}

function refreshFileInput(){
  let modal = $(".modal")
  modal.modal("hide");
  $('form p').text("Перетащите файл или нажмите на область");
  $( "#upload-input" ).val("");
}
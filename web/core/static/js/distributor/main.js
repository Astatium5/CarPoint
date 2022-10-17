$(document).ready(function(){
    $('#upload_file').change(function () {
      var preview = document.getElementById('company-image');
      var file = document.getElementById("upload_file").files[0];
      var reader = new FileReader();

      reader.onloadend = function () {
        preview.src = reader.result;
      }

      if (file) {
        reader.readAsDataURL(file);
      } else {
        preview.src = "";
      }
      preview.setAttribute("exp", "new")
    })
})

function uploadFile(){
  let file = document.getElementById("docs").files[0];
  if (!file){
    alert("Нужно выбрать файл для загрузки!");
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
              let option  = {
                animation: true,
                delay: 5000
              }
              refreshFileInput();
              if (data["response"]) {
                const myToast = document.getElementById('doneToast');
                let bsToast = new bootstrap.Toast(myToast, option);
                bsToast.show();
              }else{
                if (data["type"] == "NotDistribAccount"){
                  const myToast = document.getElementById('failToast');
                  let bsToast = new bootstrap.Toast(myToast, option);
                  bsToast.show();
                }
              }
          }
      )
    })
  }
}

function logout(){
  fetch("/logout", {
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
                window.location.replace("/distributor");
            }
        }
    )
  })
}

function closeToast(id){
  $(`#${id}`).toast("hide");
}

function refreshFileInput(){
  let modal = $(".modal");
  modal.modal("hide");
  $( "#docs" ).val("");
}


function saveCompanyData(){
  let image = document.getElementById("company-image");
  let title = document.getElementById("title-input");
  let exp = image.getAttribute("exp");
  if (exp!="new"){
    return alert("Нужно загрузить логотип компании!");
  }else if (!title.value){
    return alert("Нужно ввести название компании!");
  }else{
    let data = new FormData();
    let file = document.getElementById("upload_file").files[0];
    data.append("image", file);
    data.append("title", title.value);

    fetch("save_data", {
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
              if (data["response"]) {
                let option  = {
                  animation: true,
                  delay: 5000
                }
                const myToast = document.getElementById('doneSaveCompanyDataToast');
                let bsToast = new bootstrap.Toast(myToast, option);
                bsToast.show();
              }
          }
      )
    })
  }
}

function goBack(id){
  let bodyFont = document.getElementById(id);
  bodyFont.style.display = 'none';
  let bodyBack = document.getElementById(`body-back-${id.replace("body-font-", "")}`);
  bodyBack.style.display = 'block';
}

function goFont(id){
  let bodyFont = document.getElementById(`body-font-${id.replace("body-back-", "")}`);
  bodyFont.style.display = 'block';
  let bodyBack = document.getElementById(id);
  bodyBack.style.display = 'none';
}

function saveDsitributorDocuments(id){
  let act = document.getElementById(`act-${id}`).files[0];
  let agreement = document.getElementById(`agreement-${id}`).files[0];
  let bill = document.getElementById(`bill-${id}`).files[0];
  if (!act && !agreement && !bill){
    alert("Нужно прикрепить документ!");
  }else{
    let data = new FormData();
    data.append("id", id);
    data.append("act", act);
    data.append("agreement", agreement);
    data.append("bill", bill);

    fetch("upload_documents", {
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
              if (data["response"]) {
                window.location.replace("/distributor/orders");
              }
          }
      )
    })
  }
}
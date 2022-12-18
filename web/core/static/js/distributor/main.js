$(document).ready(function(){
    $('#upload_file').change(function () {
      var _URL = window.URL || window.webkitURL;
      var preview = document.getElementById('company-image');
      var head_preview = document.getElementById('head-company-image');
      var file = document.getElementById("upload_file").files[0];

      var reader = new FileReader();

      reader.onloadend = function () {
        preview.src = reader.result;
        head_preview.src = reader.result;
      }

      if (file) {
        reader.readAsDataURL(file);
        reader.onload = function (e) {

          //Initiate the JavaScript Image object.
          var image = new Image();

          //Set the Base64 string return from FileReader as source.
          image.src = e.target.result;

          //Validate the File Height and Width.
          image.onload = function () {
            var height = this.height;
            var width = this.width;

            if (height > 1280 || width > 1280) {
              alert("Изображение не должно достигать больше 1280px");
              return false;
            }else{
              preview.setAttribute("exp", "new")
              return true;
           }
          };
        };
      } else {
        preview.src = "";
      }
    })
})

function uploadFile(){
  let file = document.getElementById("docs").files[0];
  if (!file){
    alert("Нужно выбрать файл для загрузки!");
  }else{
    let shine_btn = document.getElementById('shine-button');
    shine_btn.innerHTML = ' <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';

    let data = new FormData();
    data.append("file", file)

    fetch("upload_csv_file", {
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
                shine_btn.innerHTML = 'Загрузить';
                return alert('Файл успешно загружен!');
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

function closeModal(id){
  $(`#${id}`).modal("toggle");
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
               return alert('Данные успешно сохранены!');
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

function distribEntryInfo(id){
    let data = new FormData();
    data.append("id", id);

    fetch("distrib_entry_info", {
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
                let car = data["entry"]["car"];
                let modal = $("#distribEntryInfoModal");
                modal.find(".modal-title").text(`Заявка #${id}`);
                modal.find("img").attr("src", car["image"]);
                modal.find(".card-title").text(`${car["title"]}`);
                modal.find(".card-text").text(`${car["body"]}; ${car["transmission"]}; ${car["engine"]["type_fuel"]}; ${car["engine"]["volume"]};
                  ${car["engine"]["power"]}; ${car["wd"]}`);
                modal.find(".price-text").text(`Цена: ${car["price"]}₽`);
                modal.modal("show");
              }
          }
      )
    })
}

function car_decrease(car_id){
  let data = new FormData();
  data.append("car_id", car_id);

  fetch("/distributor/car_decrease", {
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
              car_count = data['car_count']
              $(`#value_${car_id}`).val(car_count);
            }
        }
    )
  })
}

function car_increase(car_id){
  let data = new FormData();
  data.append("car_id", car_id);

  fetch("/distributor/car_increase", {
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
              car_count = data['car_count']
              $(`#value_${car_id}`).val(car_count);
            }
        }
    )
  })
}

document.addEventListener("DOMContentLoaded", function(event) {
  const showNavbar = (toggleId, navId, bodyId, headerId) =>{
  const toggle = document.getElementById(toggleId),
  nav = document.getElementById(navId),
  bodypd = document.getElementById(bodyId),
  headerpd = document.getElementById(headerId)
  
  // Validate that all variables exist
  if(toggle && nav && bodypd && headerpd){
  toggle.addEventListener('click', ()=>{
  // show navbar
  nav.classList.toggle('show')
  // change icon
  toggle.classList.toggle('bx-x')
  // add padding to body
  bodypd.classList.toggle('body-pd')
  // add padding to header
  headerpd.classList.toggle('body-pd')
  })
  }
  }
  
  showNavbar('header-toggle','nav-bar','body-pd','header')
  
  /*===== LINK ACTIVE =====*/
  const linkColor = document.querySelectorAll('.nav_link')
  
  function colorLink(){
  if(linkColor){
  linkColor.forEach(l=> l.classList.remove('active'))
  this.classList.add('active')
  }
  }
  linkColor.forEach(l=> l.addEventListener('click', colorLink))
  
   // Your code to run since DOM is loaded and ready
  });
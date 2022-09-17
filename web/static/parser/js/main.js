function parse(){
    var mark = $("#mark-select").val()
    
    if(!mark){
        alert("Нужно выбрать марку");
    }else{
        var modal = $(".modal")
        modal.find(".modal-title").text(mark.capitalize())
        modal.modal("show");

        var status = document.getElementById("status");
        status.innerHTML = '<span class="badge rounded-pill text-bg-warning w-100"><h6>В процессе ...</h6></span>'

        var data = new FormData(); // Init new FormData object.
        data.append("mark", mark);
        fetch("run_parse/", {
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
                    if (data["status"]) {
                        var spinner = $(".lds-ring")
                        spinner.remove()
                        status.innerHTML = '<span class="badge rounded-pill text-bg-success w-100"><h6><i class="bi bi-check2-circle"> Готово</h6></span>';
                        var time = document.getElementById("time");
                        time.innerHTML = `<span class="badge rounded-pill text-bg-secondary w-100">${data["time_string"]}</span>`
                    }
                }
            )
        })
    }
}

function close_modal(){
    window.location.reload();
}

Object.defineProperty(String.prototype, 'capitalize', {
    value: function() {
      return this.charAt(0).toUpperCase() + this.slice(1);
    },
    enumerable: false
});
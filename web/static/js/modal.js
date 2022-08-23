function showLeaveRequestModal(car_id){
    var modal = $("#lr-modal");
    var lv_btn = document.getElementById("leave-request-btn");
    lv_btn.setAttribute( "onClick", `javascript: leaveRequest(${car_id});` );
    modal.modal("show");
}

function leaveRequest(car_id){
    var name = $("#name").val();
    var city = $("#city").val();
    var tel = $("#tel1").val();
    var email = $("#email").val();
    var address = $("#address").val();
    if (!name || !city || !tel || !email || !address){
        return alert("Нужно заполнить все поля!");
    }
    var data = new FormData(); // Init new FormData object.
    data.append("car_id", car_id);
    data.append("name", name);
    data.append("city", city);
    data.append("tel", tel);
    data.append("email", email);
    data.append("address", address);
    fetch("leave_request", {
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
                if (data["response"]){
                    var modal = $("#lr-modal");
                    modal.modal("hide");
                    return alert("Заявка успешно отправлена!");
                }
            }
        )
    })
}
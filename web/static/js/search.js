const PRICE_RANGE = {
    "1": {"from": 500000,  "to": 2000000},
    "2": {"from": 2000000, "to": 4000000},
    "3": {"from": 4000000, "to": 6000000},
    "4": {"from": 6000000, "to": 0},
}


function get_marks(){
    var PriceRangeSelectBox = document.getElementById("sb-pricerange");
    var selectedValue = PriceRangeSelectBox.options[PriceRangeSelectBox.selectedIndex].value;
    if (selectedValue){
        var PriceRange = PRICE_RANGE[selectedValue];
        var MinPrice = PriceRange['from'];
        var MaxPrice = PriceRange['to'];
        fetch(`api/get_all_marks/${MinPrice}/${MaxPrice}`, {
            method: "GET",
            contentType: 'application/json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": $.cookie("csrftoken")
            },
        }).then(function (response) {
            response.json().then(
                function (data) {
                    var marks = data["all_marks"];

                    /*var dl_mark = document.getElementById('mark');
                    marks.forEach(function(item){
                        var option = document.createElement('option');
                        option.value = item;
                        dl_mark.appendChild(option);
                    });*/
                }
            )
        })
    }
}
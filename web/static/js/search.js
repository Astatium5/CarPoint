const PRICE_RANGE = {
    "1": {"min": 500000,  "max": 2000000},
    "2": {"min": 2000000, "max": 4000000},
    "3": {"min": 4000000, "max": 6000000},
    "4": {"min": 6000000, "max": 0},
}

function get_marks(){
    let PriceList = document.getElementById("sb-pricerange");
    let PriceValue = PriceList.value;
    let MarkList = document.getElementById("sb-mark");
    if (PriceValue){
        let PriceRange = PRICE_RANGE[PriceValue];
        let MinPrice = PriceRange['min'];
        let MaxPrice = PriceRange['max'];
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
                    let marks = data["all_marks"];
                    marks.sort();
                    setElements(MarkList, marks)
                }
            )
        })
    }
}

function get_cars(){
    let PriceList = document.getElementById("sb-pricerange");
    let MarkList = document.getElementById("sb-mark");
    let BodyList = document.getElementById("sb-body");
    let TypeFuelList = document.getElementById("sb-type-fuel");
    let EngineVolumeList = document.getElementById("sb-volume");
    let TransmissionList = document.getElementById("sb-transmission");

    let PriceValue = PriceList.value;
    let MarkValue = MarkList.value;
    let PriceRange = PRICE_RANGE[PriceValue];

    if (!MarkValue){
        alert("Нужно выбрать марку");
    }
    else if (!PriceValue){
        alert("Нужно выбрать ценовой диапазон!");
    }
    else{
        let MinPrice = PriceRange['min'];
        let MaxPrice = PriceRange['max'];

        fetch(`get_cars/${MinPrice}/${MaxPrice}/${MarkValue}`, {
            method: "GET",
            contentType: 'application/json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": $.cookie("csrftoken")
            },
        }).then(function (response) {
            response.json().then(
                function (data) {
                    let cars = data["cars"];

                    let SearchCarBtn = document.getElementById("search-car-btn");
                    SearchCarBtn.innerHTML = `Смотреть ${cars.length} авто`;

                    let bodies = [];
                    let type_fuel = [];
                    let engine_volume = [];
                    let transmission = [];

                    for (i = 0; i < cars.length; i++){
                        bodies.push(cars[i]['body']);
                        type_fuel.push(cars[i]['engine_type_fuel']);
                        engine_volume.push(cars[i]['engine_volume']);
                        transmission.push(cars[i]['transmission']);
                    }

                    // Filter unique values.
                    bodies = bodies.filter(uniqueArray);
                    type_fuel = type_fuel.filter(uniqueArray);
                    engine_volume = engine_volume.filter(uniqueArray);
                    transmission = transmission.filter(uniqueArray);
                    type_fuel.sort()
                    engine_volume.sort()

                    // Add new options.
                    setElements(BodyList, bodies)
                    setElements(TypeFuelList, type_fuel)
                    setElements(EngineVolumeList, engine_volume)
                    setElements(TransmissionList, transmission)
                }
            )
        })
    }
}

function get_cars_by_body(){
    let PriceList = document.getElementById("sb-pricerange");
    let MarkList = document.getElementById("sb-mark");
    let BodyList = document.getElementById("sb-body");
    let TypeFuelList = document.getElementById("sb-type-fuel");
    let EngineVolumeList = document.getElementById("sb-volume");
    let TransmissionList = document.getElementById("sb-transmission");

    let PriceValue = PriceList.value;
    let MarkValue = MarkList.value;
    let BodyValue = BodyList.value;
    let PriceRange = PRICE_RANGE[PriceValue];

    if (!MarkValue){
        alert("Нужно выбрать марку");
    }
    else if (!PriceValue){
        alert("Нужно выбрать ценовой диапазон!");
    }else if(!BodyValue){
        alert("Нужно выбрать тип кузова!");
    }
    else{
        let MinPrice = PriceRange['min'];
        let MaxPrice = PriceRange['max'];

        fetch(`get_cars_by_body/${MinPrice}/${MaxPrice}/${MarkValue}/${BodyValue}`, {
            method: "GET",
            contentType: 'application/json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": $.cookie("csrftoken")
            },
        }).then(function (response) {
            response.json().then(
                function (data) {
                    let cars = data["cars"];

                    let SearchCarBtn = document.getElementById("search-car-btn");
                    SearchCarBtn.innerHTML = `Смотреть ${cars.length} авто`;

                    let type_fuel = [];
                    let engine_volume = [];
                    let transmission = [];

                    for (i = 0; i < cars.length; i++){
                        type_fuel.push(cars[i]['engine_type_fuel']);
                        engine_volume.push(cars[i]['engine_volume']);
                        transmission.push(cars[i]['transmission']);
                    }

                    // Filter unique values.
                    type_fuel = type_fuel.filter(uniqueArray);
                    engine_volume = engine_volume.filter(uniqueArray);
                    transmission = transmission.filter(uniqueArray);
                    type_fuel.sort()
                    engine_volume.sort()

                    // Add new options.
                    setElements(TypeFuelList, type_fuel)
                    setElements(EngineVolumeList, engine_volume)
                    setElements(TransmissionList, transmission)
                }
            )
        })
    }
}

function get_cars_by_type_fuel(){
    let PriceList = document.getElementById("sb-pricerange");
    let MarkList = document.getElementById("sb-mark");
    let BodyList = document.getElementById("sb-body");
    let TypeFuelList = document.getElementById("sb-type-fuel");
    let EngineVolumeList = document.getElementById("sb-volume");
    let TransmissionList = document.getElementById("sb-transmission");

    let PriceValue = PriceList.value;
    let MarkValue = MarkList.value;
    let BodyValue = BodyList.value;
    let TypeFuelValue = TypeFuelList.value;
    let PriceRange = PRICE_RANGE[PriceValue];

    if (!MarkValue){
        alert("Нужно выбрать марку");
    }
    else if (!PriceValue){
        alert("Нужно выбрать ценовой диапазон!");
    }else if(!BodyValue){
        alert("Нужно выбрать тип кузова!");
    }
    else{
        let MinPrice = PriceRange['min'];
        let MaxPrice = PriceRange['max'];

        fetch(`get_cars_by_type_fuel/${MinPrice}/${MaxPrice}/${MarkValue}/${BodyValue}/${TypeFuelValue}`, {
            method: "GET",
            contentType: 'application/json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": $.cookie("csrftoken")
            },
        }).then(function (response) {
            response.json().then(
                function (data) {
                    let cars = data["cars"];

                    let SearchCarBtn = document.getElementById("search-car-btn");
                    SearchCarBtn.innerHTML = `Смотреть ${cars.length} авто`;

                    let engine_volume = [];
                    let transmission = [];

                    for (i = 0; i < cars.length; i++){
                        engine_volume.push(cars[i]['engine_volume']);
                        transmission.push(cars[i]['transmission']);
                    }

                    // Filter unique values.
                    engine_volume = engine_volume.filter(uniqueArray);
                    transmission = transmission.filter(uniqueArray);
                    engine_volume.sort()

                    // Add new options.
                    setElements(EngineVolumeList, engine_volume)
                    setElements(TransmissionList, transmission)
                }
            )
        })
    }
}

function get_cars_by_transmission(){
    let PriceList = document.getElementById("sb-pricerange");
    let MarkList = document.getElementById("sb-mark");
    let BodyList = document.getElementById("sb-body");
    let TypeFuelList = document.getElementById("sb-type-fuel");
    let EngineVolumeList = document.getElementById("sb-volume");
    // var EnginePowerList = document.getElementById("sb-power");
    var TransmissionList = document.getElementById("sb-transmission");

    var PriceValue = PriceList.value;
    var MarkValue = MarkList.value;
    var BodyValue = BodyList.value;
    var TypeFuelValue = TypeFuelList.value;
    var TransmissionValue = TransmissionList.value;
    var PriceRange = PRICE_RANGE[PriceValue];

    if (!MarkValue){
        alert("Нужно выбрать марку");
    }
    else if (!PriceValue){
        alert("Нужно выбрать ценовой диапазон!");
    }else if(!BodyValue){
        alert("Нужно выбрать тип кузова!");
    }else if(!TypeFuelValue){
        alert("Нужно выбрать тип двигателя!");
    }
    else{
        let MinPrice = PriceRange['min'];
        let MaxPrice = PriceRange['max'];

        fetch(`get_cars_by_transmission/${MinPrice}/${MaxPrice}/${MarkValue}/${BodyValue}/${TypeFuelValue}/${TransmissionValue}`, {
            method: "GET",
            contentType: 'application/json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": $.cookie("csrftoken")
            },
        }).then(function (response) {
            response.json().then(
                function (data) {
                    var cars = data["cars"];

                    var SearchCarBtn = document.getElementById("search-car-btn");
                    SearchCarBtn.innerHTML = `Смотреть ${cars.length} авто`;

                    var engine_volume = [];

                    for (i = 0; i < cars.length; i++){
                        engine_volume.push(cars[i]['engine_volume']);
                    }

                    // Filter unique values.
                    engine_volume = engine_volume.filter(uniqueArray);
                    engine_volume.sort()

                    // Add new options.
                    setElements(EngineVolumeList, engine_volume)
                }
            )
        })
    }
}

function get_cars_by_engine_volume(){
    let PriceList = document.getElementById("sb-pricerange");
    let MarkList = document.getElementById("sb-mark");
    let BodyList = document.getElementById("sb-body");
    let TypeFuelList = document.getElementById("sb-type-fuel");
    let EngineVolumeList = document.getElementById("sb-volume");
    let TransmissionList = document.getElementById("sb-transmission");

    let PriceValue = PriceList.value;
    let MarkValue = MarkList.value;
    let BodyValue = BodyList.value;
    let TypeFuelValue = TypeFuelList.value;
    let EngineVolumeValue = EngineVolumeList.value;
    let TransmissionValue = TransmissionList.value;
    let PriceRange = PRICE_RANGE[PriceValue];

    if (!MarkValue){
        alert("Нужно выбрать марку");
    }
    else if (!PriceValue){
        alert("Нужно выбрать ценовой диапазон!");
    }else if(!BodyValue){
        alert("Нужно выбрать тип кузова!");
    }else if(!TypeFuelValue){
        alert("Нужно выбрать тип двигателя!");
    }
    else if(!TypeFuelValue){
        alert("Нужно выбрать коробку передач!");
    }
    else{
        let MinPrice = PriceRange['min'];
        let MaxPrice = PriceRange['max'];

        fetch(`get_cars_by_engine_volume/${MinPrice}/${MaxPrice}/${MarkValue}/${BodyValue}/${TypeFuelValue}/${TransmissionValue}/${EngineVolumeValue}`, {
            method: "GET",
            contentType: 'application/json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": $.cookie("csrftoken")
            },
        }).then(function (response) {
            response.json().then(
                function (data) {
                    let cars = data["cars"];

                    let SearchCarBtn = document.getElementById("search-car-btn");
                    SearchCarBtn.innerHTML = `Смотреть ${cars.length} авто`;
                }
            )
        })
    }
}

function uniqueArray(value, index, self) {
    return self.indexOf(value) === index;
}

function selectElement(sb, valueToSelect) {
    let opt = document.createElement('option');
    opt.value = valueToSelect;
    opt.innerHTML = valueToSelect;
    sb.appendChild(opt);
    sb.value = valueToSelect;
}

function setElements(sb, values){
    let i, L = sb.options.length - 1;
    for(i = L; i >= 1; i--) {
        sb.remove(i);
    }
    if (values.length == 1){
        selectElement(sb, values[0])
    }else{
        for (let i = 0; i < values.length; i++){
            let value = values[i];
            let opt = document.createElement('option');
            opt.value = value;
            opt.innerHTML = value;
            sb.appendChild(opt);
        }
    }
}
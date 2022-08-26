const PRICE_RANGE = {
    "1": {"min": 500000,  "max": 2000000},
    "2": {"min": 2000000, "max": 4000000},
    "3": {"min": 4000000, "max": 6000000},
    "4": {"min": 6000000, "max": 0},
}

function get_marks(){
    var PriceList = document.getElementById("sb-pricerange");
    var PriceValue = PriceList.value;
    var MarkList = document.getElementById("sb-mark");
    if (PriceValue){
        var PriceRange = PRICE_RANGE[PriceValue];
        var MinPrice = PriceRange['min'];
        var MaxPrice = PriceRange['max'];
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
                    marks.sort();

                    var i, L = MarkList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        MarkList.remove(i);
                    }

                    for (var i = 0; i < marks.length; i++){
                        var opt = document.createElement('option');
                        opt.value = marks[i];
                        opt.innerHTML = marks[i];
                        MarkList.appendChild(opt);
                    }
                }
            )
        })
    }
}

function get_cars(){
    var PriceList = document.getElementById("sb-pricerange");
    var MarkList = document.getElementById("sb-mark");
    var BodyList = document.getElementById("sb-body");
    var TypeFuelList = document.getElementById("sb-type-fuel");
    var EngineVolumeList = document.getElementById("sb-volume");
    // var EnginePowerList = document.getElementById("sb-power");
    var TransmissionList = document.getElementById("sb-transmission");

    var PriceValue = PriceList.value;
    var MarkValue = MarkList.value;
    var PriceRange = PRICE_RANGE[PriceValue];

    if (!MarkValue){
        alert("Нужно выбрать марку");
    }
    else if (!PriceValue){
        alert("Нужно выбрать ценовой диапазон!");
    }
    else{
        var MinPrice = PriceRange['min'];
        var MaxPrice = PriceRange['max'];

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
                    var cars = data["cars"];

                    var SearchCarBtn = document.getElementById("search-car-btn");
                    SearchCarBtn.innerHTML = `Смотреть ${cars.length} авто`;

                    var bodies = [];
                    var type_fuel = [];
                    var engine_volume = [];
                    // var engine_power = [];
                    var transmission = [];

                    for (i = 0; i < cars.length; i++){
                        bodies.push(cars[i]['body']);
                        type_fuel.push(cars[i]['engine_type_fuel']);
                        engine_volume.push(cars[i]['engine_volume']);
                        // engine_power.push(cars[i]['engine_power']);
                        transmission.push(cars[i]['transmission']);
                    }

                    // Filter unique values.
                    bodies = bodies.filter(uniqueArray);
                    type_fuel = type_fuel.filter(uniqueArray);
                    engine_volume = engine_volume.filter(uniqueArray);
                    // engine_power = engine_power.filter(uniqueArray);
                    transmission = transmission.filter(uniqueArray);
                    type_fuel.sort()
                    engine_volume.sort()
                    // engine_power.sort()

                    // Remove old options.
                    var i, L = BodyList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        BodyList.remove(i);
                    }

                    var i, L = TypeFuelList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        TypeFuelList.remove(i);
                    }

                    var i, L = EngineVolumeList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        EngineVolumeList.remove(i);
                    }

                    /* var i, L = EnginePowerList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        EnginePowerList.remove(i);
                    } */

                    var i, L = TransmissionList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        TransmissionList.remove(i);
                    }

                    // Add new options.
                    for (var i = 0; i < bodies.length; i++){
                        var opt = document.createElement('option');
                        opt.value = bodies[i];
                        opt.innerHTML = bodies[i];
                        BodyList.appendChild(opt);
                    }

                    for (var i = 0; i < type_fuel.length; i++){
                        var opt = document.createElement('option');
                        opt.value = type_fuel[i];
                        opt.innerHTML = type_fuel[i];
                        TypeFuelList.appendChild(opt);
                    }

                    for (var i = 0; i < engine_volume.length; i++){
                        var opt = document.createElement('option');
                        opt.value = engine_volume[i];
                        opt.innerHTML = engine_volume[i];
                        EngineVolumeList.appendChild(opt);
                    }

                    /* for (var i = 0; i < engine_power.length; i++){
                        var opt = document.createElement('option');
                        opt.value = engine_power[i];
                        opt.innerHTML = engine_power[i];
                        EnginePowerList.appendChild(opt);
                    } */

                    for (var i = 0; i < transmission.length; i++){
                        var opt = document.createElement('option');
                        opt.value = transmission[i];
                        opt.innerHTML = transmission[i];
                        TransmissionList.appendChild(opt);
                    }

                    if (bodies.length == 1){
                        BodyList.value = bodies[0];
                    }
                    if (type_fuel.length == 1){
                        TypeFuelList.value = type_fuel[0];
                    }
                    if (engine_volume.length == 1){
                        EngineVolumeList.value = engine_volume[0];
                    }
                    if (transmission.length == 1){
                        TransmissionList.value = transmission[0];
                    }
                }
            )
        })
    }
}

function get_cars_by_body(){
    var PriceList = document.getElementById("sb-pricerange");
    var MarkList = document.getElementById("sb-mark");
    var BodyList = document.getElementById("sb-body");
    var TypeFuelList = document.getElementById("sb-type-fuel");
    var EngineVolumeList = document.getElementById("sb-volume");
    // var EnginePowerList = document.getElementById("sb-power");
    var TransmissionList = document.getElementById("sb-transmission");

    var PriceValue = PriceList.value;
    var MarkValue = MarkList.value;
    var BodyValue = BodyList.value;
    var PriceRange = PRICE_RANGE[PriceValue];

    if (!MarkValue){
        alert("Нужно выбрать марку");
    }
    else if (!PriceValue){
        alert("Нужно выбрать ценовой диапазон!");
    }else if(!BodyValue){
        alert("Нужно выбрать тип кузова!");
    }
    else{
        var MinPrice = PriceRange['min'];
        var MaxPrice = PriceRange['max'];

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
                    var cars = data["cars"];

                    var SearchCarBtn = document.getElementById("search-car-btn");
                    SearchCarBtn.innerHTML = `Смотреть ${cars.length} авто`;

                    var type_fuel = [];
                    var engine_volume = [];
                    // var engine_power = [];
                    var transmission = [];

                    for (i = 0; i < cars.length; i++){
                        type_fuel.push(cars[i]['engine_type_fuel']);
                        engine_volume.push(cars[i]['engine_volume']);
                        // engine_power.push(cars[i]['engine_power']);
                        transmission.push(cars[i]['transmission']);
                    }

                    // Filter unique values.
                    type_fuel = type_fuel.filter(uniqueArray);
                    engine_volume = engine_volume.filter(uniqueArray);
                    // engine_power = engine_power.filter(uniqueArray);
                    transmission = transmission.filter(uniqueArray);
                    type_fuel.sort()
                    engine_volume.sort()
                    // engine_power.sort()

                    // Remove old options.

                    var i, L = TypeFuelList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        TypeFuelList.remove(i);
                    }

                    var i, L = EngineVolumeList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        EngineVolumeList.remove(i);
                    }

                    /* var i, L = EnginePowerList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        EnginePowerList.remove(i);
                    } */

                    var i, L = TransmissionList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        TransmissionList.remove(i);
                    }

                    // Add new options.

                    for (var i = 0; i < type_fuel.length; i++){
                        var opt = document.createElement('option');
                        opt.value = type_fuel[i];
                        opt.innerHTML = type_fuel[i];
                        TypeFuelList.appendChild(opt);
                    }

                    for (var i = 0; i < engine_volume.length; i++){
                        var opt = document.createElement('option');
                        opt.value = engine_volume[i];
                        opt.innerHTML = engine_volume[i];
                        EngineVolumeList.appendChild(opt);
                    }

                    /* for (var i = 0; i < engine_power.length; i++){
                        var opt = document.createElement('option');
                        opt.value = engine_power[i];
                        opt.innerHTML = engine_power[i];
                        EnginePowerList.appendChild(opt);
                    } */

                    for (var i = 0; i < transmission.length; i++){
                        var opt = document.createElement('option');
                        opt.value = transmission[i];
                        opt.innerHTML = transmission[i];
                        TransmissionList.appendChild(opt);
                    }

                    if (type_fuel.length == 1){
                        TypeFuelList.value = type_fuel[0];
                    }
                    if (engine_volume.length == 1){
                        EngineVolumeList.value = engine_volume[0];
                    }
                    if (transmission.length == 1){
                        TransmissionList.value = transmission[0];
                    }
                }
            )
        })
    }
}

function get_cars_by_type_fuel(){
    var PriceList = document.getElementById("sb-pricerange");
    var MarkList = document.getElementById("sb-mark");
    var BodyList = document.getElementById("sb-body");
    var TypeFuelList = document.getElementById("sb-type-fuel");
    var EngineVolumeList = document.getElementById("sb-volume");
    // var EnginePowerList = document.getElementById("sb-power");
    var TransmissionList = document.getElementById("sb-transmission");

    var PriceValue = PriceList.value;
    var MarkValue = MarkList.value;
    var BodyValue = BodyList.value;
    var TypeFuelValue = TypeFuelList.value;
    var PriceRange = PRICE_RANGE[PriceValue];

    if (!MarkValue){
        alert("Нужно выбрать марку");
    }
    else if (!PriceValue){
        alert("Нужно выбрать ценовой диапазон!");
    }else if(!BodyValue){
        alert("Нужно выбрать тип кузова!");
    }
    else{
        var MinPrice = PriceRange['min'];
        var MaxPrice = PriceRange['max'];

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
                    var cars = data["cars"];

                    var SearchCarBtn = document.getElementById("search-car-btn");
                    SearchCarBtn.innerHTML = `Смотреть ${cars.length} авто`;

                    var engine_volume = [];
                    // var engine_power = [];
                    var transmission = [];

                    for (i = 0; i < cars.length; i++){
                        engine_volume.push(cars[i]['engine_volume']);
                        // engine_power.push(cars[i]['engine_power']);
                        transmission.push(cars[i]['transmission']);
                    }

                    // Filter unique values.
                    engine_volume = engine_volume.filter(uniqueArray);
                    // engine_power = engine_power.filter(uniqueArray);
                    transmission = transmission.filter(uniqueArray);
                    engine_volume.sort()
                    // engine_power.sort()

                    // Remove old options.
                    var i, L = EngineVolumeList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        EngineVolumeList.remove(i);
                    }

                    /* var i, L = EnginePowerList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        EnginePowerList.remove(i);
                    } */

                    var i, L = TransmissionList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        TransmissionList.remove(i);
                    }

                    // Add new options.
                    for (var i = 0; i < engine_volume.length; i++){
                        var opt = document.createElement('option');
                        opt.value = engine_volume[i];
                        opt.innerHTML = engine_volume[i];
                        EngineVolumeList.appendChild(opt);
                    }

                    /* for (var i = 0; i < engine_power.length; i++){
                        var opt = document.createElement('option');
                        opt.value = engine_power[i];
                        opt.innerHTML = engine_power[i];
                        EnginePowerList.appendChild(opt);
                    } */

                    for (var i = 0; i < transmission.length; i++){
                        var opt = document.createElement('option');
                        opt.value = transmission[i];
                        opt.innerHTML = transmission[i];
                        TransmissionList.appendChild(opt);
                    }

                    if (engine_volume.length == 1){
                        EngineVolumeList.value = engine_volume[0];
                    }
                    if (transmission.length == 1){
                        TransmissionList.value = transmission[0];
                    }
                }
            )
        })
    }
}

function get_cars_by_transmission(){
    var PriceList = document.getElementById("sb-pricerange");
    var MarkList = document.getElementById("sb-mark");
    var BodyList = document.getElementById("sb-body");
    var TypeFuelList = document.getElementById("sb-type-fuel");
    var EngineVolumeList = document.getElementById("sb-volume");
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
        var MinPrice = PriceRange['min'];
        var MaxPrice = PriceRange['max'];

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
                    // var engine_power = [];

                    for (i = 0; i < cars.length; i++){
                        engine_volume.push(cars[i]['engine_volume']);
                        // engine_power.push(cars[i]['engine_power']);
                    }

                    // Filter unique values.
                    engine_volume = engine_volume.filter(uniqueArray);
                    // engine_power = engine_power.filter(uniqueArray);
                    engine_volume.sort()
                    // engine_power.sort()

                    // Remove old options.
                    var i, L = EngineVolumeList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        EngineVolumeList.remove(i);
                    }

                    /* var i, L = EnginePowerList.options.length - 1;
                    for(i = L; i >= 1; i--) {
                        EnginePowerList.remove(i);
                    } */

                    // Add new options.
                    for (var i = 0; i < engine_volume.length; i++){
                        var opt = document.createElement('option');
                        opt.value = engine_volume[i];
                        opt.innerHTML = engine_volume[i];
                        EngineVolumeList.appendChild(opt);
                    }

                    /* for (var i = 0; i < engine_power.length; i++){
                        var opt = document.createElement('option');
                        opt.value = engine_power[i];
                        opt.innerHTML = engine_power[i];
                        EnginePowerList.appendChild(opt);
                    } */

                    if (engine_volume.length == 1){
                        EngineVolumeList.value = engine_volume[0];
                    }
                }
            )
        })
    }
}

function get_cars_by_engine_volume(){
    var PriceList = document.getElementById("sb-pricerange");
    var MarkList = document.getElementById("sb-mark");
    var BodyList = document.getElementById("sb-body");
    var TypeFuelList = document.getElementById("sb-type-fuel");
    var EngineVolumeList = document.getElementById("sb-volume");
    // var EnginePowerList = document.getElementById("sb-power");
    var TransmissionList = document.getElementById("sb-transmission");

    var PriceValue = PriceList.value;
    var MarkValue = MarkList.value;
    var BodyValue = BodyList.value;
    var TypeFuelValue = TypeFuelList.value;
    var EngineVolumeValue = EngineVolumeList.value;
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
    else if(!TypeFuelValue){
        alert("Нужно выбрать коробку передач!");
    }
    else{
        var MinPrice = PriceRange['min'];
        var MaxPrice = PriceRange['max'];

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
                    var cars = data["cars"];

                    var SearchCarBtn = document.getElementById("search-car-btn");
                    SearchCarBtn.innerHTML = `Смотреть ${cars.length} авто`;
                }
            )
        })
    }
}

function uniqueArray(value, index, self) {
    return self.indexOf(value) === index;
}
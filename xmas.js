function getLEDStatus() {
    var url  = "/led/";
    var xhr  = new XMLHttpRequest()
    xhr.open('GET', url, true)
    xhr.onload = function () {
	var ledStatus = JSON.parse(xhr.responseText);
	if (xhr.readyState == 4 && xhr.status == "200") {
            var leds = ledStatus.leds;
            for( var l in leds ) {
                var index = leds[ l ].index;
                var value = leds[ l ].value;
                document.getElementById( "led-" + index.toString() ).checked = ( value > 0.0 );
            }
	} else {
	    console.error(ledStatus);
	}
    }
    xhr.send(null);
}

function setLEDStatus() {
    var data = {
        leds: []
    };
    var url = "/led/";
    for( var i = 0; i < 26; ++i ) {
        var led = { index : i, value : 0.0 };
        var isOn = document.getElementById( "led-" + i.toString() ).checked;
        led.value = ( isOn ? 1.0 : 0.0 );
        data.leds.push( led );
    }
    var json = JSON.stringify(data);

    var xhr = new XMLHttpRequest();
    xhr.open("PUT", url, true);
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function () {
	var ledStatus = JSON.parse(xhr.responseText);
	if (xhr.readyState == 4 && xhr.status == "200") {
	    console.log(ledStatus);
	} else {
	    console.error(users);
	}
    }
    xhr.send(json);
}

function padDigits(number, digits) {
    return Array(Math.max(digits - String(number).length + 1, 0)).join(0) + number;
}

function startTimer(duration, display) {
	var timer = duration;
	var hours = parseInt(timer.hour)
    var minutes = parseInt(timer.minute);
    var seconds = parseInt(timer.second);

	setInterval(
	    function () {
	        seconds = seconds + 1;
	        if (seconds > 59) {
	            minutes = minutes + 1;
	            seconds = 0;
	        }
	        if (minutes > 59) {
	            minutes = 0;
	            hours = hours + 1;
	        }
	        if (hours > 24) {
	            hours = 0;
	        }
	        if (seconds == 0){
	            $("body").css("background-color", "red")
	        }
            display.text(hours + ":" + padDigits(minutes,2) + ":" + padDigits(seconds, 2));
        }
	, 1000);
}

function initiateTimer(time) {
    var display = $('#time');
    startTimer(JSON.parse(time), display);
}

jQuery(function ($) {
	$.ajax({url: "time/clock", success: initiateTimer })
});

function padDigits(number, digits) {
    return Array(Math.max(digits - String(number).length + 1, 0)).join(0) + number;
}

function startTimer(duration, display) {
	var timer = duration;
    var minutes = parseInt(timer.minute);
    var seconds = parseInt(timer.second);

	setInterval(
	    function () {
	        seconds = seconds - 1;
	        if (seconds < 0) {
	            minutes = minutes - 1;
	            seconds = 59;
	        }
	        if (seconds == 0){
	            $("body").css("background-color", "red")
	        }
            display.text(padDigits(minutes,2) + ":" + padDigits(seconds, 2));
        }
	, 1000);
}

function initiateTimer(time) {
    var display = $('#time');
    startTimer(JSON.parse(time), display);
}

jQuery(function ($) {
	$.ajax({url: "/time/utc", success: initiateTimer })
});

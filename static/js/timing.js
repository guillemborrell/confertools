var timing_data;
var clock_hours;
var clock_minutes;
var clock_seconds;
var time_display = $('#time');

function padDigits(number, digits) {
    return Array(Math.max(digits - String(number).length + 1, 0)).join(0) + number;
}

function advance_clock(hours, minutes, seconds){
    seconds = seconds - 1;
    if (seconds < 0) {
        minutes = minutes - 1;
        seconds = 59;
    }
    if (minutes < 0) {
        hours = hours - 1;
        minutes = 0;
    }
    if (hours < 0) {
        hours = 1;
    }
    if (seconds == 0){
        $("body").css("background-color", "red")
    }

    return {"hours": hours, "minutes": minutes, "seconds": seconds}
}
function second_wise(){
    ticks = advance_clock(clock_hours, clock_minutes, clock_seconds);
    clock_hours = ticks.hours;
    clock_minutes = ticks.minutes;
    clock_seconds = ticks.seconds;
    $('#time').text(
        clock_hours + ":" +
         padDigits(clock_minutes,2) + ":" +
          padDigits(clock_seconds, 2));
}

function startTimer(ajax_data) {
    console.log(ajax_data);
    $(document).prop('title', ajax_data.track.name);
    timing_data = ajax_data;
    var timer = timing_data.localtime;
    clock_hours = parseInt(timer.hour)
    clock_minutes = parseInt(timer.minute);
    clock_seconds = parseInt(timer.second);

	setInterval(second_wise, 1000);
}

function initiateTimer(time) {
    startTimer(JSON.parse(time));
}

jQuery(function ($) {
    var present_url = window.location.href;
    var split_url = present_url.split("/");
    var talk_key = split_url[split_url.length-1];
	$.ajax({url: "/timing_data/" + talk_key, success: initiateTimer })
});

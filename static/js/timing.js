var timing_data;
var talk_title = 'title';
var talk_authors = 'authors';
var current_step = 0;
var clock_year;
var clock_month;
var clock_day;
var clock_hours;
var clock_minutes;
var clock_seconds;
var time_display = $('#time');
var counter = 0;
var time_step = 10;

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
        minutes = 59;
        hours = hours - 1;
    }
    return {"hours": hours, "minutes": minutes, "seconds": seconds}
}
function second_wise(){
    ticks = advance_clock(clock_hours, clock_minutes, clock_seconds);
    counter = counter + 1;
    clock_hours = ticks.hours;
    clock_minutes = ticks.minutes;
    clock_seconds = ticks.seconds;

    $('#talk_name').text(talk_title)
    $('#talk_authors').text(talk_authors)
    if (clock_hours > 0){
	$('#time').text(
            clock_hours + ":" +
		padDigits(clock_minutes,2) + ":" +
		padDigits(clock_seconds, 2));
    }
    else{
	$('#time').text(
		padDigits(clock_minutes,2) + ":" +
		padDigits(clock_seconds, 2));	
    }
    if (counter == timing_data[current_step+1].time){
	console.log(timing_data[current_step+1].time)
	current_step = current_step+1;
	current = timing_data[current_step];
	while (current.duration == 0){
	    current_step = current_step + 1;
	    current = timing_data[current_step];
	    console.log("Skipped zero-time step");
	}
	talk_title = current.title;
	talk_authors = current.authors;
	var seconds_to_next = current.remaining;
	clock_seconds = seconds_to_next % 60;
	clock_minutes = (seconds_to_next-clock_seconds)/60%60;
	clock_hours   = (seconds_to_next-clock_minutes*60-clock_seconds)/60/60;

	$("body").css("background-color", timing_data[current_step].panel);
	if (timing_data[current_step].panel == 'yellow'){
	    $("body").css("color", "black");
	}
	else{
	    $("body").css("color", "white");
	}
    }
}

function startTimer(ajax_data) {
    timing_data = ajax_data;
    first = timing_data[current_step]
    while (first.duration == 0){
	current_step = current_step + 1;
	first = timing_data[current_step];
	console.log("Skipped zero-time step");
    }
    talk_title = first.title;
    talk_authors = first.authors;
    var seconds_to_next = Math.round(timing_data[current_step].remaining);
    clock_seconds = seconds_to_next % 60;
    clock_minutes = (seconds_to_next-clock_seconds)/60%60;
    clock_hours   = (seconds_to_next-clock_minutes*60-clock_seconds)/60/60

    var color = timing_data[current_step].panel
    $("body").css("background-color", color);
    if (color == 'yellow'){
	$("body").css("color", "black");
    }
    else{
	$("body").css("color", "white");
    }
    
    setInterval(second_wise, time_step);
}

function initiateTimer(time) {
    var timer_data = JSON.parse(time);
    
    for (i in timer_data){
	var t = timer_data[i];
	console.log(t.title + ' ' + t.panel + ' ' + t.time + ' ' + t.remaining + ' ' + t.duration)
    }
    startTimer(timer_data);
}

jQuery(function ($) {
    var present_url = window.location.href;
    var split_url = present_url.split("/");
    var talk_key = split_url[split_url.length-1];
    $.ajax({url: "/timing_data/" + talk_key, success: initiateTimer })
});

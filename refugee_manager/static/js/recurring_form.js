$(document).ready(function() {

    hide_frequency();
    $("#id_repeats_0").click(function() {
		if ($("#id_count").val() > 1) {
			show_frequency();
		} else {
			hide_frequency();
		}
	});
    $("#id_count").change(function() {
		if ($("#id_count").val() > 1) {
			show_frequency();
		} else {
			hide_frequency();
		}
	});
	$("#id_repeats_1").click(show_frequency);
    $("#id_day").datepicker();
    $("#id_until").datepicker();
});

function hide_frequency() {
    $("#frequency").hide();
}

function show_frequency() {
    $("#frequency").show();
}

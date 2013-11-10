$(document).ready(function() {

    hide_frequency();
    $("#id_repeats_0").click(function() {
		if ($("#id_count").val() > 1) {
			show_frequency();
		} else {
			hide_frequency();
		}
	});
    $("#id_count").keyup(function() {
		if ($("#id_count").val() > 1) {
			show_frequency();
		} else {
			hide_frequency();
		}
	});
	$("#id_repeats_1").click(show_frequency);
    $("#id_day").datepicker();
    $("#id_until").datepicker();

    $('#id_refugee_case').change(function() {
	if ($(this).val()) {
	    $('#id_employment_case').val('');
	}
    });

    $('#id_employment_case').change(function() {
	if ($(this).val()) {
	    $('#id_refugee_case').val('');
	}
    });
});

function hide_frequency() {
    $("#frequency").hide();
}

function show_frequency() {
    $("#frequency").show();
}

$(document).ready(function() {
    
	hide_frequency();
    $("[name='repeats']").click(show_frequency);
    $("#id_count").change(show_frequency);
});

function hide_frequency() {
    $("#frequency").hide();
}

function show_frequency() {
    $("#frequency").show();
}
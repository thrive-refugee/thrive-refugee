$(document).ready(function() {
    
	hide_occurrences_form();
    $("#add_occurrences").click(show_occurrences_form);
});

function hide_occurrences_form() {
    $("#occurrences_form").hide();
}

function show_occurrences_form() {
    $("#occurrences_form").show();
}
$(document).ready(function() {

    hide_frequency();
    $("[name='repeats']").click(show_frequency);
    $("#id_until").click(function() {
        $("input[name=repeats][value=until]").click();
    });
    $("#id_count").change(show_frequency);
    $("#id_day").datepicker();
    $("#id_until").datepicker();
});

function hide_frequency() {
    $("#frequency").hide();
}

function show_frequency() {
    $("#frequency").show();
}
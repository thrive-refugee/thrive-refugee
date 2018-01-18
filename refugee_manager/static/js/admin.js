(function ($) {
    $(document).ready(function(){

        $('.field-volunteers_list a').each(function(vols) {
            var original = this,
                names = this.text.split(', '),
                cutoff = 4;
            if (names.length > cutoff) {
                var short_names = names.slice(0, cutoff).join(', '),
                    rest_names = names.slice(cutoff).join(', '),
                    remainder = $('<a href="#"> ...</a>').click(function(e) {
                        e.preventDefault();
                        $(this).parent().html(original);
                });
                $(this).parent().html(short_names).append(remainder);
            }
        });

    });
})(django.jQuery);
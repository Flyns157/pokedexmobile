// Suggestion
$(document).ready(function () {
    $('#recherche').on('input', function () {
        var query = $(this).val();
        if (query) {
            $.ajax({
                url: '/suggest',
                data: { 'query': query },
                success: function (data) {
                    var suggestions = $('#suggestions');
                    suggestions.empty(); // Delete old suggestions
                    for (var i = 0; i < data.length; i++) {
                        suggestions.append('<a href="/fr/' + data[i][1] + '"><img src="' + data[i][2] + '" alt="' + data[i][0] + ' preview"><p>' + data[i][0] + '</p></a>');
                    }
                    suggestions.show(); // Show new suggestions
                }
            });
        } else {
            $('#suggestions').hide(); // Hide suggestions if search bar is empty
        }
    });
});
// Focus gestion
$('.search-input').focus(function () {
    $(this).parent().parent().addClass('focus');
}).blur(function () {
    $(this).parent().parent().removeClass('focus');
})
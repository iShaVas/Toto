var months = "января, февраля, марта, апреля, мая, июня, июля, августа, сентября, октября, ноября, декабря".split(", ");

$( document ).ready(function() {
    var td;
    var str_time;
    $('.get-normal-datetime-from-datetime').each(function (i){
        str_time = $(this).text() + 'Z';
        date = new Date(Date.parse(str_time));
        $(this).html(getDateText(date));
    })
    $('.get-normal-date-from-datetime').each(function (i){
        str_time = $(this).text() + 'Z';
        date = new Date(Date.parse(str_time));
        $(this).html(date.getUTCDate() + " " + months[date.getUTCMonth()] + " " + date.getUTCFullYear());
    })
});

function getDateText(date){
    s = date.getDate() + " " + months[date.getMonth()] + " ";

    hours = date.getHours();
    if (hours < 10) {s += '0' + hours + ":"} else {s += hours + ":"};

    mins = date.getMinutes();
    if (mins < 10) {s += '0' + mins} else {s += mins};

    return s;
};

/*
$(".team-score-input").keydown(function(e) {
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
             // Allow: Ctrl+C
            (e.keyCode == 67 && e.ctrlKey === true) ||
             // Allow: Ctrl+X
            (e.keyCode == 88 && e.ctrlKey === true) ||
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
}).keyup (function () {
    if (this.value.length >= 1) {
        console.log($(".team-score-input:eq(" + ($(".team-score-input").index(this) + 1) + ")"));
        $(".team-score-input:eq(" + ($(".team-score-input").index(this) + 1) + ")").focus();
        return false;
    }
});

$('.team-score-input').on('focus', function (e) {
    $(this)
        .one('mouseup', function () {
            $(this).select();
            return false;
        })
        .select();
});
*/
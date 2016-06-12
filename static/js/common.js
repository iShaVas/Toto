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
}
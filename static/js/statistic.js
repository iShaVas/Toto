$('.select-tournament').change(function() {
    window.location = $(this).val();
});

$(".team-score-input").change(function(){
    var matchId = $(this).attr('data-match-id');
    var homeScoreBet = parseInt($('#match_' + matchId + '_home').val())
    var awayScoreBet = parseInt($('#match_' + matchId + '_away').val())

    if(!(isNaN(homeScoreBet) || isNaN(awayScoreBet))){
        var data = {
            matchId: matchId,
            homeScoreBet: homeScoreBet,
            awayScoreBet: awayScoreBet
        }

        $.post('/save_bet', data, function(resp){
            console.log(resp);
        })
    }
});
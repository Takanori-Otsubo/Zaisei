$(".standard-btn").click(function() {
    var toggle_state = $(this).find('.toggle-state');
    var standard_content =$(this).find('.standard-content');
    $(standard_content).slideToggle('slow', function() {
        if($(this).css('display') == 'none'){
            $(toggle_state).text('▶');
        }else{
            $(toggle_state).text('▼');
        }   
    });
});
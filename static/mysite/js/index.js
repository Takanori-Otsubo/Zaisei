$(".archive-module-button").click(function() {
    var archive_module_button = $(this).parent().find('.archive-module-button');
    var archive_module_month = $(this).parent().find('.archive-module-month');
    $(archive_module_month).slideToggle('slow', function() {
        if($(this).css('display') == 'none'){
            $(archive_module_button).text('▶');
        }else{
            $(archive_module_button).text('▼');
        }   
    });
});
$('.modal').on('click', function(e) {
    if (!$(e.target).closest('.blackboard').length) {
        $('.modal').fadeOut(0);
    }
});
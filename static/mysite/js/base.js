$('#setting-modal').on('click', function(e) {
    if (!$(e.target).closest('.blackboard').length) {
        $('#setting-modal').fadeOut(0);
    }
});
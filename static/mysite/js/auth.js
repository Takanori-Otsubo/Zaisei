$('.modal').on('click', function(e) {
  if (!$(e.target).closest('.card-body').length) {
    $('.modal').fadeOut(0);
  }
});
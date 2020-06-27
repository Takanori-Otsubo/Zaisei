$(function(){
    $(".menu-toggle").on("click", function() {
        $(this).next().slideToggle();
    });
});
    
$(window).resize(function(){
    var win = $(window).width();
    var p = 768;
    if(win > p){
      $("#menu").show();
    } else {
      $("#menu").hide();
    }
});
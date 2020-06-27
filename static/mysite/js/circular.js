$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

$('.circular').click(function (event) {
    event.preventDefault();
    var childWindow = window.open('about:blank');
    var circular_pk = $(this).attr('id');
    var data_href = $(this).attr('data-href');
    var childTag = $(this).children('span');
    
    $.ajax({
        url:'circular/' + circular_pk + '/add_ajax/',
        method: 'POST',
        timeout: 10000,
        dataType: "json",
    }).done(function (data) {
        if (!$(childTag).hasClass('stamp')){
            $(childTag).attr('class','stamp');
        }
        childWindow.location.href = data_href;
        childWindow = null;
    }).fail(function (XMLHttpRequest, textStatus, errorThrown){
        console.log(XMLHttpRequest.status);
        console.log(textStatus);
        console.log(errorThrown);
        console.log($(this));
        childWindow.close();
        childWindow = null;
    })
});
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

$("form").submit(function(event) {
    event.preventDefault();
    var form = $(this);
    // Ajax通信を開始
    $.ajax({
        url: form.prop("action"),
        method: 'POST',
        data: form.serialize(),
        timeout: 5000,
        dataType: "text",
    })
    .done( function(data) {
        // 通信成功時の処理を記述
        location.reload();
    })
    .fail(function() {
        // 通信失敗時の処理を記述
        $('#resultPOST').text('POST処理失敗.');
    });
});

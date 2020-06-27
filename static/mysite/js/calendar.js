$('.event-day').on('click', function(e){
    var mx = e.pageX;
    var my = e.pageY;

    var event_date = $(this).find(".join-date").text();
    var event_pk = $(this).attr('event-pk');

    var join_flag = $(this).hasClass('participated') ? true: false;
    var join_value = $(this).find(".join-value").text();
    var start_date =  $(this).find(".start-date").text();
    var start_time = $(this).find(".start-time").text();
    var end_time = $(this).find(".end-time").text();
    var event_place = $(this).find(".event-place").text();
    var event_title = $(this).find(".event-title").text();
    var event_content = $(this).find(".event-content").text();
    var file_path = $(this).find(".event-file").text();

    $('#modal-event-date').html(event_date);
    $('#modal-date').html(start_date);

    function zeroPadding(numStr,length){
        return ('0000' + numStr).slice(-length);
    }
    var date = new Date();
    var today = Number(zeroPadding(String(date.getFullYear()),4) 
        + zeroPadding(String(date.getMonth() + 1),2)
        + zeroPadding(String(date.getDate()),2));
    console.log(zeroPadding(String(date.getMonth() + 1),2));
    console.log(event_date, today);
    console.log(event_date > today);
    if(today > event_date && join_flag){
        $('#join-flag').html('参加しました');
        $('#join-msg').html("<span>参加人数 : </span><span id='join-count'></span>")
        $('#join-count').html(join_value + "人");
        $('.btn-gradient-3d-orange').css({'display':'none'});
    }else if(today > event_date && !join_flag){
        $('#join-flag').html('参加しませんでした');
        $('#join-msg').html("<span>参加人数 : </span><span id='join-count'></span>")
        $('#join-count').html(join_value + "人");
        $('.btn-gradient-3d-orange').css({'display':'none'});
    }else if(today < event_date && join_flag){
        $('#join').addClass('on');
        $('#remove').removeClass('on');
        $('#join-flag').html('参加しています');
        $('#join-msg').html("<span>参加予定人数 : </span><span id='join-count'></span>")
        $('#join-count').html(join_value + "人");
    }else{
        $('#remove').addClass('on');
        $('#join').removeClass('on');
        $('#join-flag').html('参加していません');
        $('#join-msg').html("<span>参加予定人数 : </span><span id='join-count'></span>")
        $('#join-count').html(join_value + "人");
    }
    $('#modal-event-pk').html(event_pk);
    $('#modal-time').html(start_time + "~" + end_time);
    $('#modal-place').html(event_place);
    $('#modal-title').html(event_title);
    $('.modal-body').html(event_content);
    
    if (file_path){
        $('#modal-file').html('<a href="' + file_path + '">通知文</a>');
    }else{
        $('#modal-file').html('');
    }

    $('.modal').fadeIn();
    $('.modal').css({
        "position" : "fixed",
        "top" : my + "px",
        "left" : mx + "px",
        "width" : "0%",
        "height" : "0%",
        "opacity" : "0"
    }).animate({
        "top" : "0",
        "left" : "0",
        "width" : "100%",
        "height" : "100%",
        "opacity" : "1"
    },500);
});

$('.close').on('click', function(){
    $('.modal').fadeOut();
});

$('.modal').on('click', function(e) {
    if (!$(e.target).closest('.modal-content').length) {
        $('.modal').fadeOut();
    }
});

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

$("#join").click(function (event) {
    event.preventDefault();
    var event_pk = $('#modal-event-pk').text();
    var date = new Date();
    var today = Number(String(date.getFullYear()) + String(date.getMonth() + 1) + String(date.getDate()));
    var event_date = $('#modal-event-date').text();
    if($('#remove').hasClass('on') && today <= event_date){
        $.ajax({
            url:'event/' + event_pk + '/add_ajax/',
            method: 'POST',
            timeout: 10000,
            dataType: "json",
        }).done(function (data) {
            ($(`[event-pk=${event_pk}]`)).attr('class','event-day participated');
            ($(`[event-pk=${event_pk}]`)).find(".join-value").html(data.count)
            $('#join-flag').html('参加しています');
            $('#join').addClass('on');
            $('#remove').removeClass('on');
            $('#join-count').html(data.count + "人");
        }).fail(function (XMLHttpRequest, textStatus, errorThrown){
            console.log(XMLHttpRequest.status);
            console.log(textStatus);
            console.log(errorThrown);
        })
    }else if(today > event_date){
        $('#join-msg').empty();
        $('#join-msg').append('<span>参加は締め切りました</span>');
    }
});

$("#remove").click(function (event) {
    event.preventDefault();
    var event_pk = $('#modal-event-pk').text();
    var date = new Date();
    var today = Number(String(date.getFullYear()) + String(date.getMonth() + 1) + String(date.getDate()));
    var event_date = $('#modal-event-date').text();
    if($('#join').hasClass('on') && today <= event_date){
        $.ajax({
            url: 'event/' + event_pk + '/remove_ajax/',
            method: 'POST',
            timeout: 10000,
            dataType: "json",
        }).done(function (data) {
            ($(`[event-pk=${event_pk}]`)).attr('class','event-day ' + data.level_color);
            ($(`[event-pk=${event_pk}]`)).find(".join-value").html(data.count)
            $('#join-flag').html('参加していません');
            $('#remove').addClass('on');
            $('#join').removeClass('on');
            $('#join-count').html(data.count + "人");
        }).fail(function (XMLHttpRequest, textStatus, errorThrown){
            console.log(XMLHttpRequest.status);
            console.log(textStatus);
            console.log(errorThrown);
        })
    }else if(today > event_date){
        $('#join-msg').empty();
        $('#join-msg').append('<span>参加は締め切りました</span>');
    }
});
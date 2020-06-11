def my_modal():
    join_msg = "<div id='join-msg'></div>"

    link = "<div id='attendance'>" + \
           "<div id='join-flag'></div>" +\
           "<a href='#' id='join' class='btn-gradient-3d-orange'> 参加</a>" +\
           "<a href='#' id='remove' class='btn-gradient-3d-orange'>欠席</a>" + \
           "</div>"
    date = "<div id='modal-date'></div>"
    time = "<div id='modal-time'></div>"
    place = "<div id='modal-place'></div>"
    title = "<div id='modal-title'></div>"
    file = '<div id="modal-file"></div>'
    event_pk = "<div id='modal-event-pk' style='display:None;'></div>"
    event_date = "<div id='modal-event-date' style='display:None;'></div>"

    left_box = "<div id='left-box'>" +\
               f"{event_pk}{event_date}{date}{time}{place}{title}<br>{file}<br>{join_msg}{link}" +\
               "</div>"
    res = '<div class="modal" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">'
    res += '<div class="modal-dialog" role="document">'
    res += '<div class="modal-content">'
    res += f'<div class="modal-header col-4">{left_box}</div>'
    res += f'<div class="modal-body col-7">{title}</div>'
    res += '<button type="button" class="close col-1" data-dismiss="modal" aria-label="閉じる">'
    res += '<span aria-hidden="true">&times;</span>'
    res += '</button>'
    res += '</div></div></div>'
    return res

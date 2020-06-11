import calendar
from .models import Event
import locale
import datetime
from .myhtml import my_modal

locale.setlocale(locale.LC_ALL, 'ja_JP')


class Calendar(calendar.HTMLCalendar):

    def __init__(self, year, month, login_user):
        super().__init__()
        self.year = year
        self.month = month
        self.login_user = login_user

    @classmethod
    def zero_padding(cls, num_str, length):
        temp = "0000" + str(num_str)
        return temp[-length:]

    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            user_list = list(event.user.all().values_list("username", flat=True))
            join_value = len(user_list)
            join_flag = True if str(self.login_user) in user_list else False
            level = self.login_user.level if hasattr(self.login_user, 'level') else 0

            if join_flag:
                level_color = 'participated'
            elif event.join_value <= join_value:
                level_color = 'impossible'
            elif event.level > level:
                level_color = 'executive'
            else:
                level_color = 'possible'

            date_value = Calendar.zero_padding("{0:%Y}".format(event.start_time), 4) + \
                         Calendar.zero_padding("{0:%m}".format(event.start_time), 2) + \
                         Calendar.zero_padding("{0:%d}".format(event.start_time), 2)
            event_join_value = "<span class='join-value' style='display:none'>" + str(join_value) + "</span>"
            event_date = "<span class='join-date' style='display:none'>" + date_value + "</span>"
            date = "<span class='start-date' style='display:none'>" + "{0:%m月%d日}".format(event.start_time) + "</span>"
            start_time = "<span class='start-time'>" + "{0:%H:%M}".format(event.start_time) + "</span>"
            end_time = "<span class='end-time' style='display:none'>" + "{0:%H:%M}".format(event.end_time) + "</span>"
            place = "<span class='event-place'>" + event.place + "</span>"
            event_title = "<span class='event-title'>" + event.title + "</span>"
            content = "<span class='event-content' style='display:none'>" + event.content + "</span>"
            if event.file:
                event_file = "<div class='event-file' style='display:none'>" \
                             + str(event.file.url) + "</div>"
            else:
                event_file = "<div class='event-file' style='display:none'></div>"

            event_content = event_join_value + event_date \
                            + start_time + "<br>" + place + "<br>" + event_title + date \
                            + end_time + content + event_file
            day_event = "<div class='event'>{0}</div>".format(event_content)
            d += day_event

        if day != 0:
            cls = "class='event-day {0}' event-pk='{1}' ".format(level_color, str(event.pk), ) if d else ""
            return f"<td {cls}><span class='date'>{day}</span>{d}</td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

        cal = f'<table  border="0" cellpadding="0" cellspacing="0" class="calendar table">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal + my_modal()


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year=year, month=month, day=1)
    return datetime.datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    ret_date = first - datetime.timedelta(days=1)
    ret_url = 'month=' + str(ret_date.year) + '-' + str(ret_date.month)
    return ret_url


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    ret_date = last + datetime.timedelta(days=1)
    ret_url = 'month=' + str(ret_date.year) + '-' + str(ret_date.month)
    return ret_url



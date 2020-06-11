from mysite.mixins import Calendar, prev_month, next_month, get_date
from django.utils.safestring import mark_safe


def common(request):
    d = get_date(request.GET.get('month', None))
    context = {
        'con_calendar': mark_safe(Calendar(d.year, d.month, request.user).formatmonth(withyear=True)),
        'con_prev_month': prev_month(d),
        'con_next_month': next_month(d)
    }
    return context

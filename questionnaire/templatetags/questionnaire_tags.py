from django import template
from questionnaire.models import *

register = template.Library()


@register.simple_tag
def question_num(text):
    text = text.replace(' ', '')
    res = ''
    if text[0] == '問':
        res = f'<span class="q-numtag">{text[0:2]}</span>' + f'<span class="q-text">{text[2:]}</span>'
        res = f'<div class="q-label">{res}</div>'
    elif text[0] == '(':
        res = f'<span class="sq-numtag">{text[0:3]}</span>' + f'<span class="q-text">{text[3:]}</span>'
    return res


@register.simple_tag
def create_update(model, username):
    user_list = list(eval(model).user.all().values_list("username", flat=True))
    if username in user_list:
        res = model + "update_view"
    else:
        res = model + "create_view"
    return res

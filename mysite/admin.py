from django.contrib import admin
from .models import Event, Post, Category, Circular, Standard, Comment, Reply
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


class ReplyAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)


class StandardAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Circular)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Standard, StandardAdmin)
admin.site.register(Reply, ReplyAdmin)

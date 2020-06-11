from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from register.models import User
from django.utils.translation import gettext_lazy as _


class Circular(models.Model):
    title = models.CharField(max_length=20)
    user = models.ManyToManyField(User, related_name='circular_user', blank=True)
    description = models.TextField(max_length=140, null=True, blank=True)
    file = models.FileField(upload_to='mysite/file/circular',
                            validators=[FileExtensionValidator(['pdf', ])],
                            null=True, blank=True)
    published_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-published_at']

    def read_user_list(self):
        return str(",".join(list(self.user.all().values_list("username", flat=True))))

    def __str__(self):
        return self.title +\
            "[{0}]".format(str(",".join(list(self.user.all().values_list("username", flat=True)))))


class Event(models.Model):
    title = models.CharField(max_length=20)
    user = models.ManyToManyField(User, related_name='join_user',
                                  blank=True)
    place = models.CharField(max_length=20)
    content = models.TextField(max_length=1000)
    join_value = models.IntegerField(default=0)
    level = models.IntegerField(
        default=0,
        validators=[MinValueValidator(-1), MaxValueValidator(2)]
    )
    file = models.FileField(upload_to='mysite/file/event',
                            validators=[FileExtensionValidator(['pdf', ])],
                            null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="開始時間")
    end_time = models.DateTimeField(verbose_name="終了時間")

    class Meta:
        ordering = ['start_time']

    def save(self, *args, **kwargs):
        self.url = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return "{0:%Y-%m-%d}".format(self.start_time) + ":" + str(self.title)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Standard(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category_level = models.IntegerField(default=0)
    category_list = ['組織', '年中行事', '用語', '労働問題']

    class Meta:
        ordering = ['category_level']

    def __str__(self):
        return self.title

    def category(self):
        return self.category_list[self.category_level]


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='mysite/image/thumbnail',
                                  null=True, blank=True)
    user = models.ManyToManyField(User, verbose_name=_('read user'), related_name='post_user', blank=True)
    description = models.TextField(max_length=60, null=True, blank=True)
    level = models.IntegerField(default=0, null=True, blank=True)
    published_at = models.DateField(blank=True, null=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_reader_num(self):
        return str(self.user_set.count())


class Comment(models.Model):
    text = models.TextField()
    displayed_user = models.TextField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f'投稿者:{str(self.user)} 記事:{str(self.post)} 内容:{self.text}'

    def time(self):
        return self.posted_at


class Reply(models.Model):
    """返信コメント."""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'コメント:{str(self.comment)} 返信:{str(self.text)}'

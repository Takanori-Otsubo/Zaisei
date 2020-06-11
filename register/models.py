from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator


class Section(models.Model):
    name = models.CharField(
        verbose_name=_("課"),
        max_length=10
    )

    def __str__(self):
        return str(self.name)


class Department(models.Model):
    name = models.CharField(
        verbose_name=_("部"),
        max_length=10
    )

    section = models.ManyToManyField(
        to=Section,
        verbose_name=_('課'),
        related_name="D_section_set"
    )

    def __str__(self):
        return str(self.name)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name=_('氏名'),
        max_length=20,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={'unique': _("A user with that username already exists.")},
    )

    email = models.EmailField(
        verbose_name=_('メールアドレス'),
        unique=False
    )

    department = models.ForeignKey(
        to=Department,
        verbose_name=_('部'),
        on_delete=models.SET_NULL,
        null=True,
        related_name="U_department_set",
        related_query_name="U_department",
    )

    section = models.ForeignKey(
        to=Section,
        verbose_name=_('課'),
        on_delete=models.SET_NULL,
        null=True,
        related_name="U_section_set",
        related_query_name="U_section",
    )

    level = models.IntegerField(
        verbose_name=_('階級'),
        default=0,
        validators=[MinValueValidator(-1), MaxValueValidator(2)]
    )

    union_class = models.CharField(
        verbose_name=_('役職名'),
        max_length=20,
        default='なし',
        blank=True
    )

    is_staff = models.BooleanField(
        verbose_name=_('編集権'),
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name=_('アカウントの有無'),
        default=True,
    )

    date_joined = models.DateTimeField(
        verbose_name=_('アカウント作成日'),
        default=timezone.now
    )

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_belongs(self):
        return f'({str(self.department)} {str(self.section)})'

    def __str__(self):
        return self.username

    def user_detail(self):
        return {'username': self.username,
                'department': self.department,
                'section': self.section
                }
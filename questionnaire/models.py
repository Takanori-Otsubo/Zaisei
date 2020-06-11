from django.db import models
from register.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


quality_choice = (
    (0, '不満'),
    (1, 'どちらかと言えば不満'),
    (2, 'どちらとも言えない'),
    (3, 'どちらかと言えば満足'),
    (4, '満足')
)

quantity_choice = (
    (0, '少ない'),
    (1, 'どちらか言えば少ない'),
    (2, 'ちょうどよい'),
    (3, 'どちらかと言えば多い'),
    (4, '多い')
)

boolean_choice = (
    (True, 'はい'),
    (False, 'いいえ')
)


class CoronaVirusQuestion(models.Model):
    title = '新型コロナウイルス対策に関するアンケート調査'
    deadline = 20200701
    url = 'questionnaire:CoronaVirus'

    preventive_choice = (
        ('0', 'オフィスの密集を避けるための職場分散の実施'),
        ('1', 'デスク間･窓口へのパーテーション等設置'),
        ('2', '定期的な窓開け等による換気'),
        ('3', 'アルコール･除菌シート等の衛生用品の設置'),
        ('4', 'その他')
    )

    rate_choice = (
        (0, '0％(職場のほぼ誰も取得したことがない)'),
        (1, '0％~20％(毎日職場の2割以下がローテーションで取得)'),
        (2, '20％~40%(毎日職場の2割から4割程度がローテーションで取得)'),
        (3, '40％~60%(毎日職場の4割から6割程度がローテーションで取得)'),
        (4, '60%~(毎日職場の6割以上がローテーションで取得)')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )

    question1_1 = models.CharField(
        verbose_name=_('問1(1)テレワーク･時差出勤"以外"で職場で行っている感染予防対策はありますか。(複数選択可)'),
        max_length=30
    )

    question1_2 = models.CharField(
        verbose_name=_('(2)(1)で「その他」を選択した方のみお答えください。その他にどのような感染予防対策を行っていますか。'),
        max_length=100,
        blank=True
    )

    question2_1 = models.IntegerField(
        verbose_name=_('問2(1)テレワーク･時差出勤"以外"で職場で行っている感染予防対策への評価はどれくらいですか。'),
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        choices=quality_choice
    )

    question2_2 = models.CharField(
        verbose_name=_('(2)(1)で「満足」以外を選択した方のみお答えください。どのような点が不十分ですか。'),
        max_length=100,
        blank=True
    )

    question3 = models.CharField(
        verbose_name=_('問3テレワーク･時差出勤"以外"で職場で行って欲しい感染予防対策はありますか。'),
        max_length=200,
        blank=True
    )

    question4_1 = models.IntegerField(
        verbose_name=_('問4(1)職場でのテレワークの実施率はどれぐらいですか。'),
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        choices=rate_choice
    )

    question4_2 = models.IntegerField(
        verbose_name=_('(2)(1)の実施率をどう評価してますか。'),
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        choices=quantity_choice
    )

    question4_3 = models.CharField(
        verbose_name=_('(3)(2)の評価の理由はなぜですか。'),
        max_length=100,
        blank=True
    )

    question5_1 = models.BooleanField(
        verbose_name=_('問5(1)今年度あなたはテレワークを行いましたか。'),
        choices=boolean_choice
    )

    question5_2 = models.IntegerField(
        verbose_name=_('(2)(1)で「はい」の方のみお答えください。テレワークへの評価はどれくらいですか。'),
        choices=quality_choice,
        null=True
    )

    question5_3 = models.CharField(
        verbose_name=_('(3)(1)で「はい」の方のみお答えください。テレワークを行った上での不満点、またよかった点をお答えください。'),
        max_length=200,
        blank=True
    )

    question5_4 = models.CharField(
        verbose_name=_('(4)(1)で「いいえ」の方のみお答えください。それはなぜですか。'),
        max_length=50,
        blank=True
    )

    question5_5 = models.CharField(
        verbose_name=_('(5)テレワークについて職制側に提案したい改善点があればお答えください。'),
        max_length=200,
        blank=True
    )

    question6_1 = models.BooleanField(
        verbose_name=_('問6(1)今後もテレワーク業務の継続を望みますか'),
        choices=boolean_choice
    )

    question6_2 = models.CharField(
        verbose_name=_('(2)(1)の理由はなぜですか'),
        max_length=200,
        blank=True
    )

    question7_1 = models.CharField(
        verbose_name=_('問7(1)コロナ禍の情勢において、職制側に求める施策をお答えください。'),
        max_length=100,
        blank=True
    )

    question7_2 = models.CharField(
        verbose_name=_('(2)コロナ禍の情勢において、労働組合に求める働きをお答えください。'),
        max_length=100,
        blank=True
    )

    def __str__(self):
        return str(self.user)

    def to_dict(self):
        return {'回答者': str(self.user),
                '部': str(self.user.user_detail()['department']),
                '課': str(self.user.user_detail()['section']),
                '問1(1)': self.question1_1,
                '問1(2)': self.question1_2,
                '問2(1)': self.question2_1,
                '問2(2)': self.question2_2,
                '問3': self.question3,
                '問4(1)': self.question4_1,
                '問4(2)': self.question4_2,
                '問4(3)': self.question4_3,
                '問5(1)': self.question5_1,
                '問5(2)': self.question5_2,
                '問5(3)': self.question5_3,
                '問5(4)': self.question5_4,
                '問5(5)': self.question5_5,
                '問6(1)': self.question6_1,
                '問6(2)': self.question6_2,
                '問7(1)': self.question7_1,
                '問7(2)': self.question7_2
            }

    def to_list(self):
        return [
            str(self.user),
            str(self.user.user_detail()['department']),
            str(self.user.user_detail()['section']),
            self.question1_1,
            self.question1_2,
            self.question2_1,
            self.question2_2,
            self.question3,
            self.question4_1,
            self.question4_2,
            self.question4_3,
            self.question5_1,
            self.question5_2,
            self.question5_3,
            self.question5_4,
            self.question5_5,
            self.question6_1,
            self.question6_2,
            self.question7_1,
            self.question7_2
        ]
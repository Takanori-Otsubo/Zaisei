# Generated by Django 2.2.7 on 2020-05-31 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0010_coronavirusquestion_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coronavirusquestion',
            name='deadline',
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question1_1',
            field=models.CharField(max_length=30, verbose_name='問1(1)テレワーク･時差出勤"以外"で職場で行っている感染予防対策はありますか。(複数選択可)'),
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question1_2',
            field=models.CharField(blank=True, default=None, max_length=100, verbose_name='(2)(1)で「その他」を選択した方のみお答えください。その他にどのような感染予防対策を行っていますか。'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question2_2',
            field=models.CharField(blank=True, default=None, max_length=100, verbose_name='(2)(1)で「満足」以外を選択した方のみお答えください。どのような点が不十分ですか。'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question3',
            field=models.CharField(blank=True, default=None, max_length=200, verbose_name='問3テレワーク･時差出勤"以外"で職場で行って欲しい感染予防対策はありますか。'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question4_3',
            field=models.CharField(blank=True, default=None, max_length=100, verbose_name='(3)(2)の評価の理由はなぜですか。'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question5_2',
            field=models.IntegerField(blank=True, choices=[(0, '不満'), (1, 'どちらかと言えば不満'), (2, 'どちらとも言えない'), (3, 'どちらかと言えば満足'), (4, '満足')], default=None, verbose_name='(2)(1)で「はい」の方のみお答えください。テレワークへの評価はどれくらいですか。'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question5_3',
            field=models.CharField(blank=True, default=None, max_length=200, verbose_name='(3)(1)で「はい」の方のみお答えください。テレワークを行った上での不満点、またよかった点をお答えください。'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question5_4',
            field=models.CharField(blank=True, default=None, max_length=50, verbose_name='(4)(1)で「いいえ」の方のみお答えください。それはなぜですか。'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question5_5',
            field=models.CharField(blank=True, default=None, max_length=200, verbose_name='(5)テレワークについて職制側に提案したい改善点があればお答えください。'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question6_2',
            field=models.CharField(blank=True, default=None, max_length=200, verbose_name='(2)(1)の理由はなぜですか'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question7_1',
            field=models.CharField(blank=True, default=None, max_length=100, verbose_name='問7(1)コロナ禍の情勢において、職制側に求める施策をお答えください。'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coronavirusquestion',
            name='question7_2',
            field=models.CharField(blank=True, default=None, max_length=100, verbose_name='(2)コロナ禍の情勢において、労働組合に求める働きをお答えください。'),
            preserve_default=False,
        ),
    ]

from django import forms
from .models import CoronaVirusQuestion


class CoronaVirusForm(forms.ModelForm):
    class Meta:
        model = CoronaVirusQuestion
        fields = (
            'question1_1', 'question1_2',
            'question2_1', 'question2_2',
            'question3',
            'question4_1', 'question4_2', 'question4_3',
            'question5_1', 'question5_2', 'question5_3', 'question5_4', 'question5_5',
            'question6_1', 'question6_2',
            'question7_1', 'question7_2'
        )

    PREVENTIVE_CHOICES = (
        ('0', '何も行っていない'),
        ('1', 'オフィスの密集を避けるための職場分散の実施'),
        ('2', 'デスク間･窓口へのパーテーション等設置'),
        ('3', '定期的な窓開け等による換気'),
        ('4', 'アルコール･除菌シート等の衛生用品の設置'),
        ('5', 'その他')
    )

    BOOLEAN_CHOICES = (
        (True, 'はい'),
        (False, 'いいえ')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['question1_1'] = forms.MultipleChoiceField(
            label='問1(1)テレワーク･時差出勤"以外"で職場で行っている感染予防対策はありますか。(複数選択可)',
            widget=forms.CheckboxSelectMultiple(),
            choices=CoronaVirusForm.PREVENTIVE_CHOICES,
        )
        self.fields['question1_1'].required = True
        self.fields['question1_2'].required = False
        self.fields['question2_2'].required = False
        self.fields['question3'].widget.attrs['placeholder'] = '自由回答'
        self.fields['question3'].required = False
        self.fields['question5_1'].widget = forms.RadioSelect()
        self.fields['question5_1'].choices = CoronaVirusForm.BOOLEAN_CHOICES
        self.fields['question5_2'].required = False
        self.fields['question5_3'].required = False
        self.fields['question5_4'].required = False
        self.fields['question5_5'].widget.attrs['placeholder'] = '自由回答'
        self.fields['question5_5'].required = False
        self.fields['question6_1'].widget = forms.RadioSelect()
        self.fields['question6_1'].choices = CoronaVirusForm.BOOLEAN_CHOICES
        self.fields['question7_1'].widget.attrs['placeholder'] = '自由回答'
        self.fields['question7_1'].required = False
        self.fields['question7_2'].widget.attrs['placeholder'] = '自由回答'
        self.fields['question7_2'].required = False

    def clean(self):
        super().clean()
        if 'question1_1' not in self.cleaned_data:
            raise forms.ValidationError('問1(1)を入力してください。')

        q1_1 = self.cleaned_data['question1_1']
        q1_2 = self.cleaned_data['question1_2']
        q2_1 = self.cleaned_data['question2_1']
        q2_2 = self.cleaned_data['question2_2']
        q5_1 = self.cleaned_data['question5_1']
        q5_2 = self.cleaned_data['question5_2']
        q5_3 = self.cleaned_data['question5_3']
        q5_4 = self.cleaned_data['question5_4']

        if '0' in q1_1 and len(q1_1) > 1:
            raise forms.ValidationError('問1(1)に「何も行ってない」とそれ以外にチェックが入っています。')
        elif '5' in q1_1 and not q1_2:
            raise forms.ValidationError('問1(1)と(2)が矛盾しています')
        elif '5' not in q1_1 and q1_2:
            raise forms.ValidationError('問1(1)と(2)が矛盾しています')
        elif q2_1 is not 4 and not q2_2:
            raise forms.ValidationError('問2(1)と(2)が矛盾しています')
        elif q2_1 is 4 and q2_2:
            raise forms.ValidationError('問2(1)と(2)が矛盾しています')
        elif q5_1 and q5_2 is None:
            raise forms.ValidationError('問5(1)と(2)が矛盾しています')
        elif not q5_1 and q5_2 is not None:
            raise forms.ValidationError('問5(1)と(2)が矛盾しています')
        elif q5_1 and q5_3 is None:
            raise forms.ValidationError('問5(1)と(3)が矛盾しています')
        elif not q5_1 and q5_3:
            raise forms.ValidationError('問5(1)と(3)が矛盾しています')
        elif not q5_1 and not q5_4:
            raise forms.ValidationError('問5(1)と(4)が矛盾しています')
        elif q5_1 and q5_4:
            raise forms.ValidationError('問5(1)と(4)が矛盾しています')
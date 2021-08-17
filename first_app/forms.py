from django import forms

from first_app.models import Board


class PostWriteForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super(PostWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {
            'autocomplete': 'off',
            'class': 'form-control',
            'placeholder': '타이틀을 100자 이내로 입력 해주세요'
        }
        self.fields['content'].widget.attrs = {
            'autocomplete': 'off',
            'class': 'form-control',
            'placeholder': '글 내용을 적어 주세요',
            'rows': 30
        }

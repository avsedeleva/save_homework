from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text')
        '''labels = {
            'text': 'Введите текст публикации:',
            'group': 'Выберите группу:'
            }'''

    def clean_text(self): 
        data = self.cleaned_data['text'] 
        if data is None: 
            raise forms.ValidationError('Введите текст') 
        return data
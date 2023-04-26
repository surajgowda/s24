from django.forms import ModelForm, Textarea
from .models import DailyUpdate

class UpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ""
        self.fields['text'].widget.attrs.update({'class': 'form-control','placeholder':'Please update your progress'})
    class Meta:
        model = DailyUpdate
        fields = ['text'] 
        widgets = {'text': Textarea(attrs={'rows': 15}), }
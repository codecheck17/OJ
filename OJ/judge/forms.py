from email.policy import default
from django import forms
from .models import Submission

Language_Choices = {
    ('1','C++'),
    ('2','Java'),
    ('3','Python'),
    ('4','JavaScript'),
    ('5','Haskell'),
}
class CodeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['Code']
    
    Language_Select = forms.ChoiceField(choices = Language_Choices) 
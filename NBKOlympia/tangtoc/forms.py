from django.forms import ModelForm
from .models import Question

class QuestionForm(ModelForm):
    """
    Class to generate a form to create new question
    """
    
    class Meta:
        model = Question
        fields = "__all__"
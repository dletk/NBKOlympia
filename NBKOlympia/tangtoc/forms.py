from django.forms import ModelForm
from .models import Question, Answer

class QuestionForm(ModelForm):
    """
    Class to generate a form to create new question
    """
    
    class Meta:
        model = Question
        fields = "__all__"


class AnswerForm(ModelForm):
    """
    Class to generate a form to create new answer, the owner of the answer will be filled by backend view code
    """

    class Meta:
        model = Answer
        fields = ["content"]
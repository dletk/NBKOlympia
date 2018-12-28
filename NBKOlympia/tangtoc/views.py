from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy

from .forms import QuestionForm, AnswerForm


# Create your views here.
@login_required(login_url="login")
def home(request):
    """
    The main page of the program, display all information needed
    """
    return HttpResponse("This is the home page")


class NewQuestion(generic.CreateView):
    """
    Class-based view to handle creating a new question into database
    Using class-based view to have the default error handling
    """

    form_class = QuestionForm
    success_url = reverse_lazy("newQuestion")
    template_name = "baseForm.html"

    # Handle the get request to make sure only staff or admin can login to this page
    def get(self, request):
        user = request.user

        if user.is_staff or user.is_superuser:
            form = self.form_class()
            return render(request, template_name=self.template_name, context={"form": form})
        else:
            return HttpResponse("Bạn không được phép truy cập tính năng này, vui lòng liên hệ với thành viên quản lý hoặc admin")

class NewAnswer(generic.CreateView):
    """
    Class-based view to submit a new answer to the database
    """

    form_class = AnswerForm
    success_url = reverse_lazy("answer")
    template_name = "baseForm.html"


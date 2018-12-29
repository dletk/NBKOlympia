from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer

from datetime import datetime, timedelta, timezone
import json


# Global information about what is the current question being asked
currentQuestion = 0
currentRound = ""

# Create your views here.


@login_required(login_url="login")
def home(request):
    """
    The main page of the program, display all information needed
    """
    return render(request, template_name="tangtoc/home.html")


@login_required(login_url="login")
def reset(request):
    """
    The view to reset the current question to be 0, used to prepare before actual show
    """
    global currentQuestion, currentRound

    user = request.user

    # TODO: Everyone who is a staff that access the homepage will reset the current question to be 0
    if user.is_staff:
        currentQuestion = 0
        currentRound = ""
        return redirect(reverse_lazy("home"))
    else:
        return render(request, template_name="tangtoc/home.html",
                      context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})



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
            return render(request, template_name="tangtoc/home.html",
                          context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})


class NewAnswer(generic.CreateView):
    """
    Class-based view to submit a new answer to the database
    """

    form_class = AnswerForm
    success_url = reverse_lazy("answer")
    template_name = "baseForm.html"

    # Handle the post method to inlcude question number and
    def post(self, request):
        global currentQuestion, currentRound

        user = request.user
        # Get the form data submitted by user
        formAnswer = AnswerForm(request.POST)
        # Create an answer instance but not yet saved
        answer = formAnswer.save(commit=False)
        answer.owner = user
        answer.question_number = currentQuestion
        answer.round = currentRound

        # Save the answer
        answer.save()

        # Return a new page for the next question
        form = self.form_class()
        return render(request, template_name=self.template_name, context={"form": form})


@login_required(login_url="login")
def question(request, round, question_number):
    """
    View to handle displaying question. Receive a question number to notify the backend code
    """
    global currentQuestion, currentRound

    user = request.user
    # Check to make sure that only staff can access this link
    if not user.is_staff:
        return render(request, template_name="tangtoc/home.html",
                      context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})
    else:
        # Get the question out of database
        try:
            question = Question.objects.get(question_number=question_number, round=round)
            # Change current question to the question being displayed
            currentQuestion = question_number
            currentRound = round
            return render(request, template_name="tangtoc/question.html", context={"question": question})
        except ObjectDoesNotExist:
            # Handle the does not exist exception
            return render(request, template_name="tangtoc/home.html",
                          context={"message": "Xin lỗi, bạn chưa có câu hỏi số {} trong cơ sở dữ liệu cho vòng thi {}, vui lòng thêm câu hỏi.".format(question_number, round)})


def to_json_answer(answer, currentTime):
    """
    Helper method to convert an answer into JSON format
    """
    timeAnswerDelta = currentTime - answer.time_posted
    
    timeAnswer = 30 - timeAnswerDelta.total_seconds()
    if timeAnswer < 0:
        timeAnswer = 0
    return dict(owner=str(answer.owner), content=answer.content, timeAnswer="{:.3f}".format(timeAnswer))


@login_required(login_url="login")
def getAnswers(request):
    """
    Back end code for the AJAX call to get answers of question after timeout
    """
    global currentQuestion, currentRound

    user = request.user

    if not user.is_staff:
        return HttpResponse("Truy cập bị từ chối")
    else:
        # Set the time to query
        currentTime = datetime.now(timezone(timedelta(hours=7)))
        # Get all answer of the current question that is before the current time
        answers = Answer.objects.get_final_answers_for(round, currentQuestion).filter(
            time_posted__lt=currentTime).order_by("time_posted")

        result = [to_json_answer(answer, currentTime) for answer in answers]

        return JsonResponse(json.dumps(result), safe=False)

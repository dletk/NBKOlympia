from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.db.models import Q

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer
from userprofile.models import MyUser


from datetime import datetime, timedelta, timezone
import json
import random


# Global information about what is the current question being asked
currentQuestion = 0
currentQuestionContent = ""
currentRound = ""

# Create your views here.


@login_required(login_url="login")
def home(request):
    """
    The main page of the program, display all information needed
    """
    return render(request, template_name="tangtoc/home.html")


@login_required(login_url="login")
def resetQuestion(request):
    """
    The view to reset the current question to be 0, used to prepare before actual show
    """
    global currentQuestion, currentRound, currentQuestionContent

    user = request.user

    # TODO: Everyone who is a staff that access the homepage will reset the current question to be 0
    if user.is_superuser:
        currentQuestion = 0
        currentQuestionContent = ""
        currentRound = ""

        # Delete all answers
        Answer.objects.all().delete()

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
        return render(request, template_name=self.template_name, context={"form": form, "answerView": True})
    
    def get(self, request):
        form = self.form_class()
        return render(request, template_name=self.template_name, context={"form": form, "answerView": True})


@login_required(login_url="login")
def question(request, round, question_number):
    """
    View to handle displaying question. Receive a question number to notify the backend code
    """
    global currentQuestion, currentRound, currentQuestionContent

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
            currentQuestionContent = question.content
            currentRound = round


            return render(request, template_name="tangtoc/question.html", context={"question": question, "round": round})
        except ObjectDoesNotExist:
            # Handle the does not exist exception
            return render(request, template_name="tangtoc/home.html",
                          context={"message": "Xin lỗi, bạn chưa có câu hỏi số {} trong cơ sở dữ liệu cho vòng thi {}, vui lòng thêm câu hỏi.".format(question_number, round)})


@login_required(login_url="login")
def khoidong(request, thi_sinh):
    """
    Method to handle khoidong round, return the set of question related to thi_sinh
    """
    # Prevent this page from being accessed by contestant
    if request.user.is_staff:
        # Get all the questions related to this person for khoidong
        questions = Question.objects.filter(contestant=thi_sinh).filter(round="khoidong").values_list("content")
        if len(questions) == 0:
            return render(request, template_name="tangtoc/home.html",
                        context={"message": "Xin lỗi, bạn chưa có câu hỏi cho thí sinh này trong cơ sở dữ liệu cho vòng thi khoi dong, vui lòng thêm câu hỏi."})
        else:
            # Convert the querySet to list to pass to JS variable later
            return render(request, template_name="tangtoc/khoidong.html", context={"questions": json.dumps(list(questions))})
    else:
        return render(request, template_name="tangtoc/home.html",
                      context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})


def get_file_type(file_name):
    """
    Helper method to get the file type of the given file name
    """
    # +1 for the index to ignore the dot "."
    file_extension = file_name[file_name.rindex(".")+1:].lower()
    if file_extension in ["mp4", "mov"]:
        return "video"
    else:
        return "image"


def to_json_question(question):
    """
    Helper method to convert a question to JSON format
    """
    if question.file:
        return dict(content=question.content, file=question.file.url, solution=question.solution, file_type=get_file_type(question.file.url), value=question.value)
    else:
        return dict(content=question.content, file=None, solution=question.solution, file_type=None, value=question.value)


def get_3_questions(question_values):
    """
    Helper method to get 3 available questions from the database based on question values provided as a list
    [10,10,20],....
    """
    # Get all available questions for vedich
    questions_vedich = Question.objects.filter(
        round="vedich").filter(used=False)

    # Get all available questions for 10, 20, 30 value
    questions = {10: questions_vedich.filter(value=10),
                 20: questions_vedich.filter(value=20),
                 30: questions_vedich.filter(value=30)}

    list_questions = []

    for value in question_values:
        question = questions[value][random.randint(0, len(questions[value])-1)]

        list_questions.append(question)

        # Remove all the question with the same type of knowledge
        questions[10] = questions[10].exclude(
            type_knowledge=question.type_knowledge)
        questions[20] = questions[20].exclude(
            type_knowledge=question.type_knowledge)
        questions[30] = questions[30].exclude(
            type_knowledge=question.type_knowledge)
    
    # Mark all selected question as used
    for question in list_questions:
        question.used = True
        question.save()

    return [to_json_question(question) for question in list_questions]


@login_required(login_url="login")
def vedich(request, goi_cau_hoi):
    """
    Method to handle the view for vedich round, return a set of question with the current required goi_cau_hoi value
    """
    # Prevent the access of contestant
    if request.user.is_staff:
        if goi_cau_hoi == 40:
            question_value = [10,10,20]
            try:
                questions = get_3_questions(question_value)
            except ValueError:
                return render(request, template_name="tangtoc/home.html",
                              context={"message": "Xin lỗi, bạn không có đủ câu hỏi để tạo gói {} mới".format(goi_cau_hoi)})
        elif goi_cau_hoi == 60:
            question_value = [10, 20, 30]
            try:
                questions = get_3_questions(question_value)
            except ValueError:
                return render(request, template_name="tangtoc/home.html",
                              context={"message": "Xin lỗi, bạn không có đủ câu hỏi để tạo gói {} mới".format(goi_cau_hoi)})
        else:
            question_value = [20, 30, 30]
            try:
                questions = get_3_questions(question_value)
            except ValueError:
                return render(request, template_name="tangtoc/home.html",
                              context={"message": "Xin lỗi, bạn không có đủ câu hỏi để tạo gói {} mới".format(goi_cau_hoi)})
        # Convert the querySet to list to pass to JS variable later
        return render(request, template_name="tangtoc/vedich.html", context={"questions": json.dumps(questions), "values": question_value})
    else:
        return render(request, template_name="tangtoc/home.html",
                      context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})


def to_json_answer(answer, currentTime):
    """
    Helper method to convert an answer into JSON format
    """
    global currentRound

    timeAnswerDelta = currentTime - answer.time_posted
    
    if currentRound == "tangtoc":
        timeAnswer = 30 - timeAnswerDelta.total_seconds()
    elif currentRound == "vcnv":
        timeAnswer = 15 - timeAnswerDelta.total_seconds()

    if timeAnswer < 0:
        timeAnswer = 0
    return dict(owner=str(answer.owner), content=answer.content, timeAnswer="{:.3f}".format(timeAnswer))

def get_current_question(request):
    """
    Method to get the current question for AJAX to update the answer view

    Return the current question's content only, as JSON format
    """
    global currentQuestion, currentQuestionContent
    global currentRound

    result = None
    # Response the current question with json format with a get method
    if request.method == "GET":
        if currentQuestionContent == "":
            result = dict(question="")
            return JsonResponse(json.dumps(result), safe=False)
        else:
            return JsonResponse(json.dumps(dict(question=currentQuestionContent)), safe=False)
    elif request.method == "POST":
        currentQuestionContent = request.POST.get("question", "")
        return JsonResponse(json.dumps(dict(question=currentQuestionContent)), safe=False)
        
        

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
        answers = Answer.objects.get_final_answers_for(currentRound, currentQuestion).filter(
            time_posted__lt=currentTime).order_by("time_posted")

        result = [to_json_answer(answer, currentTime) for answer in answers]

        return JsonResponse(json.dumps(result), safe=False)


@login_required(login_url="login")
def updateGrade(request, username=None, value=None):
    """
    View to handle the grading to update the current grade of contestant 
    """
    if request.user.is_thuky or request.user.is_staff:
        if username is not None:
            MyUser.objects.filter(username=username).update(grade=value)
        return HttpResponse("Updated");
    else:
        return render(request, template_name="tangtoc/home.html",
                    context={"message": "Xin lỗi, bạn không được phép truy cập tính năng này"})

@login_required(login_url="login")
def grading(request):
    """
    View to display the current grading of contestant
    """
    contestants = MyUser.objects.filter(is_contestant=True)

    return render(request, template_name="tangtoc/grade.html", context={"contestants": contestants})

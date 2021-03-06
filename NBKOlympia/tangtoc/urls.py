from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("newQuestion/", login_required(views.NewQuestion.as_view(), login_url="login"), name="newQuestion"),
    path("answer/", login_required(views.NewAnswer.as_view(), login_url="login"), name="answer"),
    path("question/<str:round>/<int:question_number>/", views.question, name="question"),
    path("question/vedich/goi/<int:goi_cau_hoi>/", views.vedich, name="vedich"),
    path("question/khoidong/<str:thi_sinh>/", views.khoidong, name="khoidong"),
    path("getAnswers/", views.getAnswers, name="getAnswers"),
    path("getCurrentQuestion,", views.get_current_question, name="getCurrentQuestion"),
    path("resetQuestion/", views.resetQuestion, name="resetQuestion"),
    path("grading/", views.grading, name="grading"),
    path("updateGrade/<str:username>/<int:value>", views.updateGrade, name="updateGrade"),
    path("updateGrade/", views.updateGrade, name="updateGrade")
]

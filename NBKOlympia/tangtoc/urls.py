from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("newQuestion/", login_required(views.NewQuestion.as_view(), login_url="login"), name="newQuestion"),
    path("answer/", login_required(views.NewAnswer.as_view(), login_url="login"), name="answer"),
    path("question/<int:question_number>", views.question, name="question"),
    path("getAnswers/", views.getAnswers, name="getAnswers"),
]

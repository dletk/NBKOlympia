from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="login")
def home(request):
    """
    The main page of the program, display all information needed
    """
    return HttpResponse("This is the home page")

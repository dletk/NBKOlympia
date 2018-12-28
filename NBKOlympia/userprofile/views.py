from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from django.views import generic
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


# Create your views here.

# Sign up view, using built-in class based view so it is easier to maintain and deploy
# Read more here: https://docs.djangoproject.com/en/2.0/topics/class-based-views/intro/
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "baseForm.html"

    def get(self, request):
        # Customize the get method, the post method is handled for us by built-in function

        if request.user.is_authenticated:
            # Redirect user to the profile page if they already login and try to sign up
            return redirect("home")
        else:
            form = self.form_class()
            return render(request, self.template_name, {"form": form})


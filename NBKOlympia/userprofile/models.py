from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.
def user_directory_path(instance, filename):
    """
    Method to return the path as MEDIA_ROOT/<username>/filename
    """
    return "userprofile/{}/{}".format(instance.username, filename)

class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    The user model for the whole application. Also can be used in the admin interface.
    Extending PermissionsMixin to grant the proper permission to different type of users
    """

    # Basic information of user
    username = models.CharField(max_length=40, unique=True, blank=False)
    first_name = models.CharField(max_length=40, blank=False)
    last_name = models.CharField(max_length=40, blank=False)
    email = models.CharField(max_length=150, blank=True)
    # The profile picture and the date of birth can be i=empty
    profile_pic = models.ImageField(null=True, blank=True, upload_to=user_directory_path, default="userprofile/default_profile.jpg")

    # Management variables for django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # The manager to control the objects created using this model
    objects = UserManager()
    # The identifier of this model in the database, using username for simplicity
    USERNAME_FIELD = "username"
    # Email field is required
    EMAIL_FIELD = "email"
    # Must-have information when creating an account
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self):
        return self.first_name + " " + self.last_name

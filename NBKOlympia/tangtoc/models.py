from django.db import models


def question_directory_path(instance, filename):
    """
    Method to return the path as MEDIA_ROOT/<username>/filename
    """
    return "tangtoc/{}/{}".format(instance.question_number, filename)

class Question(models.Model):
    """
    The model for storing a question in the database
    """

    # The text content of this question
    content = models.TextField(verbose_name="Câu hỏi", blank=False)
    # The index of this question. In real use, there are only 4 questions numbered 1-4
    question_number = models.IntegerField(verbose_name="Câu hỏi số", unique=True, blank=False, primary_key=True)
    # Question file (for video question or question with image)
    file = models.FileField(verbose_name="File đính kèm", upload_to=question_directory_path, blank=True)

    #  Solution
    solution = models.CharField(verbose_name="Đáp án", blank=False, max_length=255)

    objects = models.Manager()

    def __str__(self):
        return str(self.question_number) + ": " + self.content

class Answer(models.Model):
    """
    The model for all user answers
    """
    # Content of the answer, cannot be blank.
    content = models.CharField(max_length=255, blank=False, verbose_name="Đáp án")

    # Time posted to server, so we can see who is the first
    time_posted = models.DateTimeField(verbose_name="Thời gian trả lời", auto_now_add=True, blank=False)

    # Question number, used to filter all answers for the same question
    question_number = models.IntegerField(verbose_name="Câu hỏi số", blank=False)

    # User, who is the owner of this answer
    owner = models.ForeignKey("userprofile.MyUser", on_delete=models.CASCADE)

    # Model manager
    objects = models.Manager()

    def __str__(self):
        """
        toString method for an answer
        """
        return "Câu hỏi {}, thí sinh: {}, đáp án: {}".format(self.question_number, self.owner, self.content)
from django.db import models
from userprofile.models import MyUser


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
    question_number = models.IntegerField(
        verbose_name="Câu hỏi số", blank=False)
    # Round
    round = models.CharField(max_length=255, verbose_name="Vòng thi", choices=[(
        "tangtoc", "Tăng tốc"), ("vcnv", "VCNV"), ("khoidong", "Khởi động"), ("vedich", "Về đích")], blank=False)

    # Some question is assigned directly to a contestant
    contestant = models.CharField(max_length=255, verbose_name = "Thí sinh",  blank=True, choices=[
                                  ("ts1", "Thí sinh 1"), ("ts2", "Thí sinh 2"), ("ts3", "Thí sinh 3"), ("ts4", "Thí sinh 4")])
    # Question file (for video question or question with image)
    file = models.FileField(verbose_name="File đính kèm",
                            upload_to=question_directory_path, blank=True)

    # TODO: Make a field for type of knowledge
    type_knowledge = models.CharField(max_length=255, verbose_name="Lĩnh vực", blank=True, choices = [
        ("toan", "toan"), ("ly", "ly"), ("hoa", "hoa"), ("anh", "anh"), ("van", "van"), ("su", "su"), ("sinh", "sinh"), ("dia", "dia"), ("tin", "tin"), ("theduc-quocphong", "theduc-quocphong"), ("cau_hoi_chung", "cau_hoi_chung")], null=True)

    # Value of the question
    value = models.IntegerField(verbose_name="Giá trị câu hỏi", choices=[(10,10),(20,20),(30,30)], blank=True, null=True)

    # Boolean value indicating whether the question is used
    used = models.BooleanField(verbose_name="Đã sử dụng", blank=False, default=False)

    #  Solution
    solution = models.CharField(
        verbose_name="Đáp án", blank=False, max_length=255)

    objects = models.Manager()

    class Meta:
        unique_together = (("question_number", "round"),)

    def __str__(self):
        return str(self.round) + ": " + str(self.question_number) + ": " + self.content


class AnswerManager(models.Manager):
    """
    Custom manager to work with answers model
    """

    def get_final_answers_for(self, round, question_number):
        """
        Return the query set of final answers from all contestant for this question, sorted by time.
        """
        # Get all the contestant
        contestants = MyUser.objects.filter(is_contestant=True)

        # An empty queryset to contains all returned answers
        final_querySet = self.none()

        for person in contestants:
            # Sort by -time_posted to get the most recent one
            last_answer = self.filter(question_number__iexact=question_number).filter(
                round=round).filter(owner=person).order_by("-time_posted").first()
            if last_answer is not None:
                final_querySet |= self.filter(pk=last_answer.pk)

        # Sort the query set by time posted before return
        final_querySet = final_querySet.order_by("time_posted")

        return final_querySet


class Answer(models.Model):
    """
    The model for all user answers
    """
    # Content of the answer, cannot be blank.
    content = models.CharField(
        max_length=255, blank=False, verbose_name="Đáp án")

    # Time posted to server, so we can see who is the first
    time_posted = models.DateTimeField(
        verbose_name="Thời gian trả lời", auto_now_add=True, blank=False)

    # Question number, used to filter all answers for the same question
    question_number = models.IntegerField(
        verbose_name="Câu hỏi số", blank=False)

    # Round
    round = models.CharField(max_length=255, verbose_name="Vòng thi", choices=[
                             ("tangtoc", "Tăng tốc"), ("vcnv", "VCNV"), ("khoidong", "Khởi động"), ("vedich", "Về đích"), ("", "Empty")], blank=False)

    # User, who is the owner of this answer
    owner = models.ForeignKey("userprofile.MyUser", on_delete=models.CASCADE)

    # Model manager
    objects = AnswerManager()

    def __str__(self):
        """
        toString method for an answer
        """
        return "Câu hỏi {}, thí sinh: {}, đáp án: {}".format(self.question_number, self.owner, self.content)

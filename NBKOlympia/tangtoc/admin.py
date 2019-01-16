from django.contrib import admin
from .models import Question, Answer

# Register your models here.
def marks_all_as_unused(modeladmin, request, queryset):
    """
    Method to mark all selected questions as un used
    """
    queryset.update(used=False)

marks_all_as_unused.short_description = "Đánh dấu câu hỏi là chưa sử dụng"

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["content", "round", "used", "contestant"]
    ordering = ["round"]
    actions = [marks_all_as_unused]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["content", "round", "question_number", "owner"]
    ordering = ["-time_posted"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

admin.site.site_header = "NBK OLYMPIA - Trang quản lý"

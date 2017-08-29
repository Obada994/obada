from django.contrib import admin
from .models import Question, Choice, Answer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline,)

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Answer)
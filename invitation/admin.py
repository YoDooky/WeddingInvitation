from django.contrib import admin
from invitation.models import UserSurvey, SurveyQuestion, SurveyAnswer, SurveyResponse


class QuestionTabAdmin(admin.TabularInline):
    model = SurveyQuestion
    fields = ['text', 'is_selected']
    extra = 1


class AnswerTabAdmin(admin.TabularInline):
    model = SurveyAnswer
    fields = ['text']
    extra = 1


class ResponseTabAdmin(admin.TabularInline):
    model = SurveyResponse
    fields = ['question', 'answer']
    extra = 1


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerTabAdmin]


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSurvey)
class UserSurveyAdmin(admin.ModelAdmin):
    inlines = [ResponseTabAdmin]

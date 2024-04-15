from django.db import models
from django.core.exceptions import ValidationError


class SurveyQuestion(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

    objects = models.Manager()


class SurveyAnswer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(to=SurveyQuestion, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text

    objects = models.Manager()


class SurveyResponse(models.Model):
    user = models.ForeignKey(to='UserSurvey', on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(to=SurveyQuestion, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(to=SurveyAnswer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.question} - {self.answer}'

    objects = models.Manager()


class UserSurvey(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    session_key = models.CharField(max_length=100, default=None, null=True, blank=True)
    response = models.ForeignKey(to=SurveyResponse, on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()

    def clean(self):
        if len(self.first_name) <= 2:
            raise ValidationError('Имя должно содержать больше двух символов')
        if len(self.last_name) <= 2:
            raise ValidationError('Фамилия должна содержать больше двух символов')
        if any(char.isdigit() for char in self.first_name):
            raise ValidationError('Имя не должно содержать цифры')
        if any(char.isdigit() for char in self.last_name):
            raise ValidationError('Фамилия не должна содержать цифры')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

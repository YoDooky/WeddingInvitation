from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError
import re

from invitation import utils
from invitation.models import UserSurvey, SurveyResponse, SurveyQuestion, SurveyAnswer


def handle_invitiation(req):
    user_session_key = req.session.session_key

    first_name = req.POST.get('first_name', None)
    last_name = req.POST.get('last_name', None)

    # find user in db
    user = UserSurvey.objects.filter(
        first_name=first_name,
        last_name=last_name,
        session_key=user_session_key
    ).first()
    alert = ''
    # if user already exist then send responses from db to js
    if user:
        user_responses = SurveyResponse.objects.filter(user_id=user.id).all()
        questions = []
        for response in user_responses:
            questions.append(f'question{response.question_id}-option{response.answer_id}')
        alert = ''
        response_data = {
            'message': 'Вы уже были зарегестрированы. Измените свои предпочтения если нужно',
            'alert': alert,
            'questions': questions
        }
        return JsonResponse(response_data)

    # if user doesn't exist then create
    else:
        # create new user creds for db
        user_instance = UserSurvey(
            first_name=first_name,
            last_name=last_name,
            session_key=user_session_key
        )
        try:
            user_instance.clean()
            user_instance.save()
        except ValidationError as ex:
            alert = str(*ex)
        response_data = {
            'message': 'Пожалуйста отметьте свои предпочтения',
            'alert': alert
        }
        return JsonResponse(response_data)


def handle_survey(req):
    user_session_key = req.session.session_key
    notification_message = 'Спасибо что придете, будем рады видеть вас'

    first_name = req.POST.get('first_name', None)
    last_name = req.POST.get('last_name', None)

    # find user in db
    user = UserSurvey.objects.filter(
        first_name=first_name,
        last_name=last_name,
        session_key=user_session_key
    ).first()

    # survey instance
    survey_instances = []

    # find user responses
    user_responses = SurveyResponse.objects.filter(user_id=user.id).all()

    # write user choices to db
    for data in req.POST:
        if 'form_data' not in data:
            continue
        # get filled form data from js POST request
        qa_data = req.POST.get(data, None)
        if qa_data:
            question_id = int(re.findall(r'\d+', qa_data)[0])
            answer_id = int(re.findall(r'\d+', qa_data)[1])
            # update user responses if they are already exists
            if user_responses.exists():
                for response in user_responses:
                    if response.question_id == question_id:
                        response.answer_id = answer_id
                        survey_instances.append(response)
                        break
                notification_message = 'Ваши пожелания обновлены'
            # save new user responses
            else:
                survey_q = SurveyQuestion.objects.get(pk=question_id)
                survey_a = SurveyAnswer.objects.get(pk=answer_id)
                survey_r = SurveyResponse(
                    user=user,
                    question=survey_q,
                    answer=survey_a
                )
                survey_instances.append(survey_r)

    # check if all questions was answered then save to db
    alert = ""
    if len(survey_instances) == SurveyQuestion.objects.count():
        for instance in survey_instances:
            instance.save()
    else:
        alert = "Не на все вопросы были даны ответы"

    response_data = {
        'message': notification_message,
        'alert': alert
    }
    return JsonResponse(response_data)


def index(request):
    survey = SurveyQuestion.objects.all()
    if not survey:
        utils.init_db_data()
        survey = SurveyQuestion.objects.all()

    if request.method == 'POST':
        # request to get post request for register and render survey
        if request.POST.get('action', '') == 'register':
            return handle_invitiation(request)
        # request to get post request and finalize survey
        if request.POST.get('action', '') == 'survey':
            return handle_survey(request)

    data = {
        'title': 'WeddingInvitation',
        'survey': survey,
    }
    return render(request, 'index.html', context=data)

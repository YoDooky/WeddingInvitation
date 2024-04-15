from invitation.models import SurveyQuestion, SurveyAnswer


def init_db_data():
    """
    Fills db with standart questions and answers
    """
    question = [
        SurveyQuestion.objects.create(
            text="Потребуется ли вам трансфер от ЗАГСа до коттеджа?",
        ),
        SurveyQuestion.objects.create(
            text="Какой алкоголь вы предпочитатете?",
        ),
        SurveyQuestion.objects.create(
            text="Необходимо ли вам размещение в коттедже на ночь? ",
        )
    ]

    SurveyAnswer.objects.create(
        text="Да",
        question=question[0]
    )
    SurveyAnswer.objects.create(
        text="Нет",
        question=question[0]
    )

    SurveyAnswer.objects.create(
        text="Красное вино",
        question=question[1]
    )
    SurveyAnswer.objects.create(
        text="Красное вино",
        question=question[1]
    )
    SurveyAnswer.objects.create(
        text="Белое вино",
        question=question[1]
    )
    SurveyAnswer.objects.create(
        text="Шампанское",
        question=question[1]
    )
    SurveyAnswer.objects.create(
        text="Водка",
        question=question[1]
    )
    SurveyAnswer.objects.create(
        text="Джин",
        question=question[1]
    )
    SurveyAnswer.objects.create(
        text="Не буду пить алкоголь",
        question=question[1]
    )

    SurveyAnswer.objects.create(
        text="Да",
        question=question[2]
    )
    SurveyAnswer.objects.create(
        text="Нет",
        question=question[2]
    )

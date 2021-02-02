import pytest

from content.models import Poll, Question, Answer, UserAnswer


@pytest.mark.django_db
def test_poll_model():
    poll = Poll(
        title="Опрос",
        description="Пусто",
        start="2021-01-12 00:00",
        finish="2021-01-15 00:00",
    )

    assert str(poll) == poll.title


@pytest.mark.django_db
def test_question_model():
    poll = Poll(
        title="Опрос",
        description="Пусто",
        start="2021-01-12 00:00",
        finish="2021-01-15 00:00",
    )
    question = Question(
        text="Вопрос", type_q="Ответ с выбором одного варианта", poll=poll
    )

    assert str(question) == question.text


@pytest.mark.django_db
def test_answer_model():
    poll = Poll(
        title="Опрос",
        description="Пусто",
        start="2021-01-12 00:00",
        finish="2021-01-15 00:00",
    )
    question = Question(
        text="Вопрос", type_q="Ответ с выбором одного варианта", poll=poll
    )
    answer = Answer(variant="Вариант 1", question=question)

    assert str(answer) == answer.variant


@pytest.mark.django_db
def test_user_answer_model():
    poll = Poll(
        title="Опрос",
        description="Пусто",
        start="2021-01-12 00:00",
        finish="2021-01-15 00:00",
    )
    question = Question(
        text="Вопрос", type_q="Ответ с выбором одного варианта", poll=poll
    )
    answer = Answer(variant="Вариант 1", question=question)
    user_answer = UserAnswer(answer=answer)

    assert str(user_answer) == user_answer.answer.variant

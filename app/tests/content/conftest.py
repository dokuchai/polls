import pytest
from datetime import datetime, timedelta
from content.models import Poll, Question, Answer, UserAnswer


@pytest.fixture(scope="function")
def add_poll():
    def _add_poll(title):
        now = datetime.now()
        poll = Poll.objects.create(
            title=title, description="Тест", start=now, finish=now + timedelta(days=7)
        )
        return poll

    return _add_poll


@pytest.fixture(scope="function")
def add_question(add_poll):
    def _add_question():
        poll = add_poll("Опрос")
        question = Question.objects.create(text="Вопрос 1", poll=poll)
        return question

    return _add_question


@pytest.fixture(scope="function")
def add_answer(add_question):
    def _add_answer(variant):
        answer = Answer.objects.create(variant=variant, question=add_question())
        return answer

    return _add_answer


@pytest.fixture(scope="function")
def add_auth_user_answer(api_client):
    def _add_auth_user_answer(add_answer, token):
        api_client.force_authenticate(token=token, user=token.user)
        user_answer = UserAnswer.objects.create(user=token.user, answer=add_answer)
        return user_answer

    return _add_auth_user_answer


@pytest.fixture(scope="function")
def add_anonymous_user_answer(api_client):
    def _add_anonymous_user_answer(add_answer, anonymous_id):
        user_answer = UserAnswer.objects.create(
            anonymous=anonymous_id, answer=add_answer
        )
        return user_answer

    return _add_anonymous_user_answer

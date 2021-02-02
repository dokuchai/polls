import pytest
from datetime import datetime, timedelta
from content.models import Poll, Question, Answer, UserAnswer


@pytest.mark.django_db
def test_get_active_polls(api_client, add_poll):
    poll = add_poll("Опрос")
    response = api_client.get("/active-polls/")

    assert response.status_code == 200
    assert response.data[0]["title"] == poll.title


@pytest.mark.django_db
def test_get_retrieve_poll(api_client, add_answer):
    answer = add_answer("Вариант")

    response = api_client.get(f"/polls/{answer.question.poll.id}/")

    assert response.status_code == 200
    assert response.data["title"] == answer.question.poll.title
    assert response.data["questions"][0]["text"] == answer.question.text
    assert response.data["questions"][0]["answers"][0]["variant"] == answer.variant


@pytest.mark.django_db
def test_add_poll(api_client, add_admin_token):
    token = add_admin_token()
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.post(
        "/polls/",
        {
            "title": "Опрос 1",
            "description": "Описание",
            "start": datetime.now(),
            "finish": datetime.now() + timedelta(days=7),
        },
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_update_poll(api_client, add_admin_token, add_poll):
    token = add_admin_token()
    poll = add_poll("Опрос 1")
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.patch(f"/polls/{poll.id}/", {"title": "Новый опрос"})

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_poll(api_client, add_admin_token, add_poll):
    token = add_admin_token()
    poll = add_poll("Новый опрос")
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.delete(f"/polls/{poll.id}/")

    assert response.status_code == 204


@pytest.mark.django_db
def test_add_question(api_client, add_admin_token, add_poll):
    token = add_admin_token()
    poll = add_poll("Опрос первый")
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.post("/questions/", {"text": "Вопрос 1", "poll": poll.id})

    assert response.status_code == 201


@pytest.mark.django_db
def test_update_question(api_client, add_admin_token, add_question):
    token = add_admin_token()
    question = add_question()
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.patch(
        f"/questions/{question.id}/", {"text": "Обновленный вопрос"}
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_question(api_client, add_admin_token, add_question):
    token = add_admin_token()
    question = add_question()
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.delete(f"/questions/{question.id}/")

    assert response.status_code == 204


@pytest.mark.django_db
def test_add_answer(api_client, add_admin_token, add_question):
    token = add_admin_token()
    question = add_question()
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.post(
        "/answers/", {"variant": "Первый вариант", "question": question.id}
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_update_answer(api_client, add_admin_token, add_answer):
    token = add_admin_token()
    answer = add_answer("Вариант 1")
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.patch(f"/answers/{answer.id}/", {"variant": "Новый вариант"})

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_answer(api_client, add_admin_token, add_answer):
    token = add_admin_token()
    answer = add_answer("Вариант")
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.delete(f"/answers/{answer.id}/")

    assert response.status_code == 204


@pytest.mark.django_db
def test_add_select_answer_auth_user(api_client, add_user_token, add_answer):
    token = add_user_token()
    answer = add_answer("Вариант")
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.post(
        "/send-answer/", {"user": token.user.id, "answer": answer.id}
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_add_input_answer_auth_user(api_client, add_user_token, add_answer):
    token = add_user_token()
    answer = add_answer("Вариант")
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.post(
        "/send-answer/", {"user": token.user.id, "text": "Ответ на вопрос"}
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_fail_add_select_answer_invalid_auth_user(
    api_client, add_user_token, add_answer
):
    token = add_user_token()
    answer = add_answer("Вариант 1")
    api_client.force_authenticate(token=token, user=token.user)

    response = api_client.post("/send-answer/", {"user": "1e", "answer": answer.id})

    assert response.status_code == 400


@pytest.mark.django_db
def test_add_select_answer_anonymous_user(api_client, add_answer):
    answer = add_answer("Вариант 1")

    response = api_client.post(
        "/send-answer/", {"anonymous": 12345678, "answer": answer.id}
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_add_input_answer_anonymous_user(api_client, add_answer):
    answer = add_answer("Вариант 1")

    response = api_client.post(
        "/send-answer/", {"anonymous": 12345678, "text": "Ответ"}
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_fail_add_select_answer_invalid_anonymous_user(api_client, add_answer):
    answer = add_answer("Вариант")

    response = api_client.post(
        "/send-answer/", {"anonymous": "1d12312", "answer": answer.id}
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_get_all_passed_polls_by_auth_user(
    api_client, add_answer, add_user_token, add_auth_user_answer
):
    token = add_user_token()
    user_answer_1 = add_auth_user_answer(
        add_answer=add_answer("Первый вариант"), token=token
    )
    user_answer_2 = add_auth_user_answer(
        add_answer=add_answer("Второй вариант"), token=token
    )

    response = api_client.get("/passed-polls/")

    assert response.status_code == 200
    assert (
        response.data[0]["questions"][0]["answers"][0]["variant"]
        == user_answer_1.answer.variant
    )
    assert (
        response.data[1]["questions"][0]["answers"][0]["variant"]
        == user_answer_2.answer.variant
    )


@pytest.mark.django_db
def test_get_all_passed_polls_by_anonymous_user(
    api_client, add_answer, add_anonymous_user_answer
):
    anonymous_id = 12345
    user_answer1 = add_anonymous_user_answer(
        anonymous_id=anonymous_id, add_answer=add_answer("Вариант 1")
    )
    user_answer2 = add_anonymous_user_answer(
        anonymous_id=anonymous_id, add_answer=add_answer("Вариант 2")
    )

    response = api_client.get(f"/passed-polls/anonymous/{anonymous_id}/")

    assert response.status_code == 200
    assert (
        response.data[0]["questions"][0]["answers"][0]["variant"]
        == user_answer1.answer.variant
    )
    assert (
        response.data[1]["questions"][0]["answers"][0]["variant"]
        == user_answer2.answer.variant
    )

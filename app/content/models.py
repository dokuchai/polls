from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    title = models.CharField("Название", max_length=120)
    description = models.TextField("Описание", blank=True, default="")
    start = models.DateTimeField("Начало")
    finish = models.DateTimeField("Окончание")

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPE = (
        ("Ответ текстом", "Ответ текстом"),
        ("Ответ с выбором одного варианта", "Ответ с выбором одного варианта"),
        (
            "Ответ с выбором нескольких варинатов",
            "Ответ с выбором нескольких варинатов",
        ),
    )
    text = models.TextField("Текст вопроса")
    type_q = models.CharField(
        "Тип вопроса", max_length=36, choices=TYPE, default="Ответ текстом"
    )
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, verbose_name="Опрос", related_name="questions"
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text


class Answer(models.Model):
    variant = models.TextField("Вариант ответа")
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Вопрос",
        related_name="answers",
    )

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.variant


class UserAnswer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        related_name="user",
    )
    anonymous = models.PositiveIntegerField(
        "ID анонимного пользователя", blank=True, null=True
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name="Ответ",
        related_name="user_answers",
        blank=True,
        null=True,
    )
    text = models.TextField("Текст", default="")

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"

    def __str__(self):
        return self.answer.variant

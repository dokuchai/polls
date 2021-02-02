from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from content.models import Answer, Poll, Question, UserAnswer
from content.serializers import (ActivePollsSerializer, AnswerCRDSerializer,
                                 PollCreateSerializer, PollDetailSerializer,
                                 PollUpdateSerializer, QuestionCRDSerializer,
                                 UserAnswerCreateSerializer)


class ActivePollsView(ListAPIView):
    """Список активных опросов"""

    serializer_class = ActivePollsSerializer
    queryset = Poll.objects.filter(
        start__lte=datetime.now(), finish__gte=datetime.now()
    )


class PollDetailView(viewsets.ModelViewSet):
    """Просмотр, изменение и удаление опроса. Изменение и удаление доступно только администратору"""

    queryset = Poll.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            permission_classes = [AllowAny]
            return PollDetailSerializer
        if self.action == "partial_update":
            permission_classes = [IsAdminUser]
            return PollUpdateSerializer
        if self.action == "destroy":
            permission_classes = [IsAdminUser]
            return PollDetailSerializer


class PollsView(viewsets.ModelViewSet):
    """Создание опроса (доступно администратору)"""

    queryset = Poll.objects.all()
    serializer_class = PollCreateSerializer
    permission_classes = [IsAdminUser]


class QuestionView(viewsets.ModelViewSet):
    """Создание, редактирование и удаление вопроса у опроса (доступно администратору)"""

    queryset = Question.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = QuestionCRDSerializer


class AnswerView(viewsets.ModelViewSet):
    """Создание, редактирование и удаление варианта ответа на вопрос (доступно администратору)"""

    queryset = Answer.objects.all()
    serializer_class = AnswerCRDSerializer
    permission_classes = [IsAdminUser]


class UserAnswerCreate(viewsets.ModelViewSet):
    """Запись ответа пользователя на вопрос"""

    serializer_class = UserAnswerCreateSerializer

    def get_queryset(self):
        if self.action == "create":
            if self.request.user:
                UserAnswer.objects.create(
                    user=self.request.user,
                    answer=self.request.data.get("answer"),
                    text=self.request.data.get("text"),
                )
            else:
                UserAnswer.objects.create(
                    anonymous=self.request.get("anonymous"),
                    answer=self.request.data.get("answer"),
                    text=self.request.data.get("text"),
                )


class PassedPollsView(viewsets.ModelViewSet):
    """Список пройденных авторизованным пользователем опросов"""

    serializer_class = PollDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return Poll.objects.filter(
                questions__answers__user_answers__user=self.request.user
            )


class PassedPollsAnonymousView(viewsets.ModelViewSet):
    """Список пройденных анонимным пользователем опросов"""

    serializer_class = PollDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            return Poll.objects.filter(
                questions__answers__user_answers__anonymous=self.kwargs["pk"]
            )

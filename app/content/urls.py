from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from content.views import (ActivePollsView, AnswerView,
                           PassedPollsAnonymousView, PassedPollsView,
                           PollDetailView, PollsView, QuestionView,
                           UserAnswerCreate)

urlpatterns = format_suffix_patterns(
    [
        path("active-polls/", ActivePollsView.as_view()),
        path("polls/", PollsView.as_view({"post": "create"})),
        path(
            "polls/<int:pk>/",
            PollDetailView.as_view(
                {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
            ),
        ),
        path("questions/", QuestionView.as_view({"post": "create"})),
        path(
            "questions/<int:pk>/",
            QuestionView.as_view(
                {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
            ),
        ),
        path("answers/", AnswerView.as_view({"post": "create"})),
        path(
            "answers/<int:pk>/",
            AnswerView.as_view(
                {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
            ),
        ),
        path("send-answer/", UserAnswerCreate.as_view({"post": "create"})),
        path("passed-polls/", PassedPollsView.as_view({"get": "list"})),
        path(
            "passed-polls/anonymous/<int:pk>/",
            PassedPollsAnonymousView.as_view({"get": "list"}),
        ),
    ]
)

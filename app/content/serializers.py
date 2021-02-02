from rest_framework import serializers
from content.models import Poll, Question, Answer, UserAnswer


class ActivePollsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ("id", "text", "type_q", "answers")


class PollDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ("id", "title", "description", "start", "finish", "questions")


class PollCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ("title", "description", "start", "finish")


class PollUpdateSerializer(PollCreateSerializer):
    start = serializers.DateTimeField(read_only=True)


class QuestionCRDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("text", "poll", "type_q")


class AnswerCRDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("variant", "question")


class UserAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ("user", "answer", "anonymous")

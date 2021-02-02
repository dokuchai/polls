from django.contrib import admin

from content.models import Answer, Poll, Question, UserAnswer


@admin.register(Poll)
class AdminPoll(admin.ModelAdmin):
    # readonly_fields = ("start",)
    pass


@admin.register(Question)
class AdminQuestion(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AdminAnswer(admin.ModelAdmin):
    pass


@admin.register(UserAnswer)
class AdminUserAnswer(admin.ModelAdmin):
    pass

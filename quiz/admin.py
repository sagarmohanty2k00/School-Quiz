from django.contrib import admin
from .models import Quiz, Questions, AppearedQuizzes, Answers
# Register your models here.


admin.site.register(Quiz)
admin.site.register(Questions)
admin.site.register(AppearedQuizzes)
admin.site.register(Answers)


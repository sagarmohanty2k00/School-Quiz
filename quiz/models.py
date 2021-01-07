from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    name = models.CharField(max_length=100, unique=True)
    pass_marks = models.IntegerField()

    def __str__(self):
        return self.name

class Questions(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    question_text = models.CharField(max_length=500)
    option_A = models.CharField(max_length=100)
    option_B = models.CharField(max_length=100)
    option_C = models.CharField(max_length=100)
    option_D = models.CharField(max_length=100)

    answer_A = models.BooleanField()
    answer_B = models.BooleanField()
    answer_C = models.BooleanField()
    answer_D = models.BooleanField()


    def __str__(self):
        return self.question_text





class AppearedQuizzes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    date = models.DateField(null=True)
    time_taken = models.IntegerField(default=0)

    marks = models.IntegerField()

    def __str__(self):
        return self.quiz.name

class Answers(models.Model):
    appeared_quiz = models.ForeignKey(AppearedQuizzes, on_delete=models.CASCADE)

    question_text = models.ForeignKey(Questions, on_delete=models.CASCADE)

    answer_A = models.BooleanField()
    answer_B = models.BooleanField()
    answer_C = models.BooleanField()
    answer_D = models.BooleanField()

    correct = models.BooleanField()






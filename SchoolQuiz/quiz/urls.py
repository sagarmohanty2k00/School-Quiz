from django.urls import path, include
from . import views

urlpatterns = [
    # User URLs
    path('signin-form/', views.signin),
    path('', views.dashboard),
    path('register-form/', views.register),
    path('login/', views.logIn),
    path('logout/', views.logOut),
    path('signup/', views.addUser),

    # Admin related URLs
    path('addquiz/', views.addQuizForm),
    path('addquizsubmit/', views.addQuizSubmit),
    path('addquestions/<int:id>', views.addQuestionsForm),
    path('editquiz/<int:id>', views.editQuiz),
    path('deletequiz/<int:id>', views.deleteQuiz),

    # Student related URLs
    path('appearquiz/<int:id>', views.appearQuiz),
    path('appearquiz/<int:qzid>/<int:qnid>/checkquiz/',  views.checkQuestion),
    path('appearquiz/<int:qzid>/<int:qnid>/', views.appearQuestion),
    path('quizdetails/<int:id>/', views.viewQuiz),
    path('result/<int:qzid>/', views.result),
    path('leaderboard/', views.leaderboard)

]
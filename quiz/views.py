from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_protect

from .models import Quiz, Questions, AppearedQuizzes, Answers

import datetime

# Create your views here.

# User Authentication
def signin(request):
    return render(request, 'loginRegister.html', {'method': 'login'})

def register(request):
    users = User.objects.all()

    return render(request, 'loginRegister.html', {'method': 'register'})

@csrf_protect
def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully")
            return redirect('/')

        else:
            messages.error(request, "Invalid credentials")
            return redirect('/signin-form')

    else:
        messages.error(request, "Something Went Wrong!!")
        return redirect('/')

def logOut(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('/')

def addUser(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password = request.POST['password']

        users = User.objects.all()
        user_list = []
        for user in users :
            user_list.append(user.username)
        if username in user_list :
            messages.success(request, "Username Exists")
            return redirect('/register-form/')

        myUser = User.objects.create_user(username, email, password)
        myUser.first_name = fname
        myUser.last_name = lname

        myUser.school_admin = True


        myUser.save()
        messages.success(request, "User Created")
        return redirect('/signin-form/')
        # messages.success(request, "Account has been created successfully")
    else:
        pass

def dashboard(request):
    user = ''
    appeared_quiz = {}
    if request.user.is_authenticated:
        user = request.user
        appeared_quiz = AppearedQuizzes.objects.filter(user=user)


    all_quiz = Quiz.objects.all()
    available = len(all_quiz)

    all_not_appeared_quiz = []
    all_appeared_quiz = []
    quiz_details = {}
    if len(appeared_quiz) == 0:
        for quiz in all_quiz:
            all_not_appeared_quiz.append(quiz)

    else:
        for quiz in all_quiz:
            query = appeared_quiz.filter(quiz=quiz)
            if query:
                all_appeared_quiz.append(quiz)
                quiz_details[quiz.name] : {
                    'name': quiz.name,
                    'marks':query.Marks,
                }

            else:
                all_not_appeared_quiz.append(quiz)


    constraints = {
        'available': available,
        'user': user,
        'all_appeared_quiz' : all_appeared_quiz,
        'all_not_appeared_quiz' : all_not_appeared_quiz,
        'no_appeared_quiz': len(all_appeared_quiz),
        'no_not_appeared_quiz' : len(all_not_appeared_quiz),
        'appeared_quizzes' : appeared_quiz,
        }

    
    
    return render(request, 'home.html', constraints)



# Adding and Removing Quizzes ( Only for Admin )
@csrf_protect
def addQuizSubmit(request):
    if request.method == "POST":
        name = request.POST['name']
        passmarks = request.POST['passmarks']

        quiz = Quiz(name=name, pass_marks=passmarks)
        quiz.save()

        
        for i in range(10):
            question = request.POST['question-'+str(i + 1)]
            op1 = request.POST['op1-'+str(i + 1)]
            op2 = request.POST['op2-'+str(i + 1)]
            op3 = request.POST['op3-'+str(i + 1)]
            op4 = request.POST['op4-'+str(i + 1)]

            q = Questions(quiz=quiz, question_text=question, option_A=op1, option_B=op2, option_C=op3, option_D=op4, answer_A=True, answer_B=False, answer_C=False, answer_D=False)
            q.save()

        return render(request, 'quizDone.html')

def addQuizForm(request):
    return render(request, 'quizDetails.html', {'mode': 'add', 'range' : ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']})

def addQuestionsForm(request, id):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'addAppearQuiz.html', {'mode': 'add', 'i':0})


@csrf_protect
def deleteQuiz(request, id):
    quiz = Quiz.objects.get(id=id)
    quiz.delete()
    quiz.save()

    return redirect("/")

def editQuiz(request, id):
    quiz = Quiz.objects.get(id=id)
    quiz.delete()

    return redirect("/")




# Student Only Section ( Appear and View Quiz )
def appearQuestion(request, qzid, qnid):
    quiz = Quiz.objects.get(id = qzid)
    questions = Questions.objects.filter(quiz=quiz)

    allquestions = []
    for q in questions:
        allquestions.append(q)

    if qnid > len(allquestions):
        return render(request, '404.html')


    appeared = AppearedQuizzes.objects.filter(user=request.user)

    if not appeared:
        return render(request, '404.html')

    if qnid == len(allquestions):
        last = True
    else:
        last = False


    constraints = {
        'name' : quiz.name,
        'question' : allquestions[qnid - 1],
        'number' : qnid,
        'mode': 'appear',
        'last': last,
    }


    return render(request, 'addAppearQuiz.html', constraints)

def viewQuiz(request, id):
    quiz = Quiz.objects.get(id=id)
    query = AppearedQuizzes.objects.filter(user=request.user).filter(quiz=quiz)
    for iterator in query:
        appearQuiz = iterator

    if appearQuiz:
        appeared = "YES"
    else:
        appeared = "NO"

    qns = Questions.objects.filter(quiz=quiz)
    questions = []
    for question in qns:
        questions.append(question)

    all_answers = Answers.objects.filter(appeared_quiz=appearQuiz) 

    result = []
    result_unit = {}

    rng = len(questions)
    for i in range(rng):
        result_unit = {}
        result_unit['id'] = i+1
        result_unit['question'] = questions[i].question_text
        for ans in Answers.objects.filter(question_text=questions[i]).filter(appeared_quiz=appearQuiz):
            answer = ans
        
        if answer.correct == True:
            result_unit['answer'] = "Correct"
        elif answer.correct == False:
            result_unit['answer'] = "Wrong"

        else:
            return HttpResponse("Something went wrong")
        
        result.insert(i, result_unit)


    constraints = {
        'mode' : 'view',
        'name' : quiz.name,
        'appeared': appeared,
        'passmarks' : quiz.pass_marks,
        'marks' : appearQuiz.marks,

        'results' : result,
    }
    return render(request, 'quizDetails.html', constraints)


def checkQuestion(request, qzid, qnid):
    if request.method == 'POST':
        quiz = Quiz.objects.get(id = qzid)
        for iterator in AppearedQuizzes.objects.filter(user=request.user).filter(quiz=quiz):
            appearQuiz = iterator

        questions = Questions.objects.filter(quiz=quiz)

        last = len(questions)

        allquestions = []
        for question in questions:
            allquestions.append(question)
        question = allquestions[qnid - 1]

        a = request.POST.get("op1")
        b = request.POST.get("op2")
        c = request.POST.get("op3")
        d = request.POST.get("op4")

        time = request.POST.get("time")


        answer = Answers()
        answer.appeared_quiz = appearQuiz
        answer.question_text = question

        yourAnwerString = ''
        if str(a) == 'on':
            yourAnwerString = yourAnwerString + 'a'
            answer.answer_A = True
        else:
            answer.answer_A = False
        if str(b) == 'on':
            yourAnwerString = yourAnwerString + 'b'
            answer.answer_B = True
        else:
            answer.answer_B = False
        if str(c) == 'on':
            yourAnwerString = yourAnwerString + 'c'
            answer.answer_C = True
        else:
            answer.answer_C = False
        if str(d) == 'on':
            yourAnwerString = yourAnwerString + 'd'
            answer.answer_D = True
        else:
            answer.answer_D = False

        originalAnswerString = ''
        ansList = []
        if question.answer_A == True:
            originalAnswerString = originalAnswerString + 'a'
            ansList.append(question.option_A)
        if question.answer_B == True:
            originalAnswerString = originalAnswerString + 'b'
            ansList.append(question.option_B)

        if question.answer_C == True:
            originalAnswerString = originalAnswerString + 'c'
            ansList.append(question.option_C)

        if question.answer_D == True:
            originalAnswerString = originalAnswerString + 'd'
            ansList.append(question.option_D)


        if yourAnwerString == originalAnswerString:
            message = 'Correct Answer'
            appearQuiz.marks = appearQuiz.marks + 10
            appearQuiz.save()
            answer.correct = True

        else:
            message = 'Wrong Answer'
            answer.correct = False

        
        answer.save()
        appearQuiz.time_taken += int(time)
        appearQuiz.save()


        

        constraints = {
            'message' : message,
            'question' : question.question_text,
            'ansList' : ansList,
            'qzid' : qzid,
            'qnid' : qnid+1,
            'last': last,
        }

        
        return render(request, 'answer.html', constraints)

    return render(request,'404.html')


def result(request, qzid):
    quiz = Quiz.objects.get(id=qzid)
    query = AppearedQuizzes.objects.filter(user=request.user).filter(quiz=quiz)
    for q in query:
        appearedQuiz = q

    constraints = {
        'quiz' : quiz,
        'passmarks' : quiz.pass_marks,
        'yourmarks' : appearedQuiz.marks,
    }
    return render(request, 'result.html', constraints)


def leaderboard(request):
    users = User.objects.all()
    leaderboard = {
        100: ['sagar', 'asutosh'],

        102: ['brad', 'pit'],

        99: ['sonu', 'sudh']
    }

    constraints = {
        'list' :sorted(leaderboard)
    }

    return render(request, 'leaderboard.html', constraints)


# APIs
#-----------------------------------------#


def appearQuiz(request, id):
    quiz = Quiz.objects.get(id=id)


    appeared_quiz = AppearedQuizzes(quiz=quiz, user=request.user, marks=0)

    appeared_quiz.save()


    return redirect(f'/appearquiz/{quiz.id}/{1}/')
from flask import Flask
from flask import render_template , request, redirect, url_for
from flask_login import login_required, logout_user, current_user
from flask import current_app as app
from models.model import *
import datetime


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_authenticated:
        quizes = Quiz.query.all()
        questions = Question.query.all()
        quiz_list = [{"questions":[question.id for question in questions if question.quiz_id == quiz.id], "id":quiz.id, "chapter": quiz.chapter.name, "date_of_quiz": quiz.date_of_quiz, "time_duration": quiz.time_duration, "remarks": quiz.remarks} for quiz in quizes]

        return render_template("user/dashboard.html" , quizes = quiz_list)
    
    return redirect(url_for("index"))

@app.route("/quiz/<int:id>")
@login_required
def quiz_start(id):
    if current_user.is_authenticated:
        quiz = Quiz.query.get(id)
        questions = Question.query.all()
        quiz_questions = [question for question in questions if question.quiz_id == quiz.id]
        return render_template("user/quiz.html", quiz = quiz, questions = quiz_questions)
    
    return redirect(url_for("index"))
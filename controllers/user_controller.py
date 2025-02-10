from flask import Flask, jsonify
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
        questions = Question.query.filter_by(quiz_id=id).all()
        quiz_questions = {"time" : quiz.time_duration, "questions":[{"id": question.id ,"question_statement": question.question_statement , "option1":question.option1, "option2":question.option2, "option3":question.option3, "option4": question.option4} for question in questions]}

        return render_template("user/quiz.html", quiz_questions = quiz_questions)
    
    return redirect(url_for("index"))

@app.route("/view-quiz/<int:id>")
@login_required
def view_quiz(id):
    if current_user.is_authenticated:
        quiz = Quiz.query.get(id)
        questions = str(Question.query.filter_by(quiz_id=id).count())
        chapter = Chapter.query.filter_by(id=quiz.chapter_id).first()
        subject_name = str(Subject.query.filter_by(id=chapter.subject_id).first().name)
        quiz_details = {"id":quiz.id ,"subject":subject_name ,"chapter":chapter.name, "question_count":questions, "date":quiz.date_of_quiz, "time":quiz.time_duration, "remarks":quiz.remarks}

        return render_template("user/view_quiz.html", quiz = quiz_details)
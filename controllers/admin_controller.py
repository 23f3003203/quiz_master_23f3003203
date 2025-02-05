from flask import current_app as app, render_template, request, redirect, url_for, flash, jsonify
from models.model import *

@app.route("/admin/dashboard")
def admin_dashboard():
    subjects = get_subjects()
    return render_template("admin/dashboard.html", subjects= subjects)

@app.route("/admin/add_subject", methods= ["POST", "GET"])
def add_subject():
    if request.method == 'POST':
        id = request.form['subject_id']
        subject_name = request.form['subject_name']
        description = request.form['description']

        existing_subject = Subject.query.filter_by(id=id).first()

        if existing_subject:
            flash("subject Already Exits.." ,"error")
            return redirect(request.url)
        
        else:
            new_subject = Subject(id=id, name = subject_name, description = description)
            db.session.add(new_subject)
            db.session.commit()
            flash("subject Added Succeffully.." ,"success")
            return redirect(request.url)

    return render_template("admin/add_subject.html")


@app.route("/admin/add_chapter" , methods = ["POST", "GET"])
def add_chapter():
    if request.method=='POST':
        subject_id = request.args.get('subject_id')
        chapter_name = request.form['chapter_name']
        id = request.form['id']
        description = request.form['description']

        existing_chapter = Chapter.query.filter_by(id=id).first()

        if existing_chapter:
            flash("Chapter Already Exits" , "error")
            return redirect(request.url)
        
        else:
            new_chapter = Chapter(id=id, name = chapter_name, description = description, subject_id=subject_id)
            db.session.add(new_chapter)
            db.session.commit()
            flash("Chapter Added Succeffully.." ,"success")
            return redirect(request.url)
         
    return render_template("admin/add_chapter.html")


@app.route("/admin/quiz", methods = ["POST", "GET"])
def quiz():
    return render_template("/admin/quiz.html")

@app.route("/admin/add_quiz", methods = ["POST", "GET"])
def add_quiz():
    return render_template("/admin/add_quiz.html")


@app.route("/admin/add_question", methods = ["POST", "GET"])
def add_question():
    return render_template("/admin/add_question.html")

def get_subjects():

    subjects = Subject.query.all()
    chapters = Chapter.query.all()

    subject_list = [{"id": subject.id, "name": subject.name, "description": subject.description, "chapter": [{"name": chapter.name, "description": chapter.description} for chapter in chapters if chapter.subject_id == subject.id]} for subject in subjects]
    chapters_list = [{"id": chapter.id, "name": chapter.name, "description": chapter.description, "subject_id" : chapter.subject_id} for chapter in chapters]
    return subject_list




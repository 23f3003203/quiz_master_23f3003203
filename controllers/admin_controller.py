from flask import current_app as app, render_template, request, redirect, url_for, flash, jsonify
from models.model import *

@app.route("/admin/dashboard")
def admin_dashboard():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    questions = Question.query.all()

    subject_list = [{"id":subject.id, "name": subject.name,"chapters" :[{"id":chapter.id, "name": chapter.name , "questions":[question.id for question in questions if question.chapter_id == chapter.id]} for chapter in chapters if chapter.subject_id == subject.id] } for subject in subjects]
    return render_template("admin/dashboard.html", subjects = subject_list)

@app.route("/admin/add_subject", methods= ["POST", "GET"])
def add_subject():
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        description = request.form['description']

        new_subject = Subject(name = subject_name, description = description)
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
        description = request.form['description']
        existing_chapter = Chapter.query.filter(Chapter.name==chapter_name, Chapter.subject_id==subject_id).first()

        if existing_chapter:
            flash("Chapter Already Exits" , "error")
            return redirect(request.url)
        
        else:
            new_chapter = Chapter(name = chapter_name, description = description, subject_id=subject_id)
            db.session.add(new_chapter)
            db.session.commit()
            flash("Chapter Added Succeffully.." ,"success")
            return redirect(request.url)
         
    return render_template("admin/add_chapter.html")


@app.route("/admin/quiz", methods = ["POST", "GET"])
def quiz():
    quizes = db.session.query(Quiz, Chapter).join(Chapter).all()
    questions = Question.query.all()
    
    quiz_list = [{"questions": [{"id": question.id ,"question_statement": question.question_statement } for question in questions if question.quiz_id == quiz.id] ,"id":quiz.id, "chapter": chapter.name, "date_of_quiz": quiz.date_of_quiz, "time_duration": quiz.time_duration} for quiz, chapter in quizes]

    return render_template("/admin/quiz.html" , quizes = quiz_list)

@app.route("/admin/add-quiz", methods = ["POST", "GET"])
def add_quiz():
    if request.method == "POST":
        chapter_id = int(request.form['chapter'])
        date_of_quiz_str = request.form['date_of_quiz']
        time_duration = request.form['time']
        remarks = request.form['remarks']

        date_of_quiz = datetime.strptime(date_of_quiz_str, '%Y-%m-%d').date()

        new_quiz = Quiz(chapter_id = chapter_id, date_of_quiz = date_of_quiz, time_duration = time_duration, remarks = remarks)
        db.session.add(new_quiz)
        db.session.commit()
        flash("Quiz Added Successfully", "success")
        return redirect(request.url) 

    subjects = Subject.query.all()
    return render_template("/admin/add_quiz.html", subjects = subjects)


@app.route("/admin/add-question", methods = ["POST", "GET"])
def add_question():
    if request.method == "POST":
        quiz_id = request.args.get('quiz_id')
        question_statement = request.form['question_statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct-option']
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        chapter_id = quiz.chapter_id

        if not quiz_id:
            flash("Quiz is required", "error")
            return redirect(request.url)
        
        if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            flash("All fields are required", "error")
            return redirect(request.url)

        new_question = Question(quiz_id = quiz_id,chapter_id = chapter_id, question_statement = question_statement, option1 = option1, option2 = option2, option3 = option3, option4 = option4, correct_option = correct_option)
        db.session.add(new_question)
        db.session.commit()
        flash("Question Added Successfully", "success")
        return redirect(request.url)
    
    return render_template("/admin/add_question.html")


@app.route("/admin/delete-chapter", methods = ["POST", "GET"])
def delete_chapter():
    chapter_id = request.args.get('id')
    if not chapter_id:
        return redirect(url_for('admin_dashboard'))
    
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    if not chapter:
        return redirect(url_for('admin_dashboard'))
    
    db.session.query(Question).filter(Question.chapter_id == chapter_id).delete()
    db.session.query(Quiz).filter(Quiz.chapter_id == chapter_id).delete()
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route("/admin/edit-chapter", methods = ["POST", "GET"])
def edit_chapter():
    chapter_id = request.args.get('id')

    if not chapter_id:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == "POST":
        chapter_name = request.form['chapter_name']
        description = request.form['description']

        chapter = Chapter.query.filter_by(id=chapter_id).first()
        chapter.name = chapter_name
        chapter.description = description
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    
    chapter = Chapter.query.filter_by(id=chapter_id).first()

    return render_template("admin/edit_chapter.html", chapter=chapter)

@app.route("/admin/get-chapters", methods = ["POST", "GET"])
def get_chapters():
    subject_id = request.args.get('subject_id')
    if not subject_id:
        chapters = Chapter.query.all()
        chapters = [{"id":chapter.id, "name": chapter.name, "description": chapter.description} for chapter in chapters]
        return jsonify(chapters)

    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    chapter_list = [{"id":chapter.id, "name": chapter.name, "description": chapter.description} for chapter in chapters]
    return jsonify(chapter_list)


@app.route("/admin/delete-question", methods = ["POST", "GET"])
def delete_question():
    question_id = request.args.get('id')
    if not question_id:
        return redirect(url_for('quiz'))
    
    question = Question.query.filter_by(id=question_id).first()
    if not question:
        return redirect(url_for('quiz'))
    
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('quiz'))


@app.route("/admin/edit-question", methods = ["POST", "GET"])
def edit_question():
    question_id = request.args.get("id")

    if not question_id:
        return redirect(url_for('quiz'))
    
    question = Question.query.filter_by(id=question_id).first()
    if not question:
        return redirect(url_for('quiz'))
    
    question_dict = {"id": question.id, "question_statement": question.question_statement, "option1": question.option1, "option2": question.option2, "option3": question.option3, "option4": question.option4, "correct_option": question.correct_option}

    if request.method == "POST":
        question_statement = request.form['question_statement']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct-option']

        if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            flash("All fields are required", "error")
            return redirect(request.url)

        question = Question.query.filter_by(id=question_id).first()
        question.question_statement = question_statement
        question.option1 = option1
        question.option2 = option2
        question.option3 = option3
        question.option4 = option4
        question.correct_option = correct_option

        db.session.commit()
        flash("Question Updated Successfully", "success")
        return redirect(request.url)
    
    return render_template("admin/edit_question.html", question=question_dict)
    




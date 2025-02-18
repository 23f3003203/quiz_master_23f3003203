from flask import current_app as app, render_template, request, redirect, url_for, flash, jsonify
from models.model import *
from datetime import date



@app.route("/admin/dashboard")
def admin_dashboard():

    if request.args.get("q"):
        id = request.args.get("q")
        subject = db.session.query(Subject).filter(Subject.id == id).first()

        if subject:
            subject_list = [{"id": id, "name": subject.name, "chapters": get_chapters(id)}]

            return render_template("admin/dashboard.html", subjects = subject_list)


    subjects = db.session.query(Subject).all()
    subject_list = [{"id":subject.id, "name": subject.name, "chapters" : get_chapters(subject.id)} for subject in subjects]
    
    return render_template("admin/dashboard.html", subjects = subject_list)



@app.route("/admin/quiz", methods = ["POST", "GET"])
def quiz():
    q = request.args.get("q")

    if q == "all":
        quizes = db.session.query(Quiz, Chapter).join(Chapter).all()
        quiz_list = [{"questions": get_questions(quiz.id) ,"id":quiz.id, "chapter": chapter.name, "date_of_quiz": quiz.date_of_quiz, "time_duration": quiz.time_duration} for quiz, chapter in quizes]

        return render_template("/admin/quiz.html" , quizes = quiz_list)
    
    if q:
        quizes = db.session.query(Quiz, Chapter).join(Chapter).filter(Quiz.chapter_id == q).all()
        quiz_list = [{"questions": get_questions(quiz.id), "id":quiz.id, "chapter": chapter.name, "date_of_quiz": quiz.date_of_quiz, "time_duration": quiz.time_duration} for quiz, chapter in quizes]
        return render_template("/admin/quiz.html" , quizes = quiz_list)

    

    quizes = db.session.query(Quiz, Chapter).join(Chapter).filter(Quiz.date_of_quiz >= date.today()).all()
    quiz_list = [{"questions": get_questions(quiz.id) ,"id":quiz.id, "chapter": chapter.name, "date_of_quiz": quiz.date_of_quiz, "time_duration": quiz.time_duration} for quiz, chapter in quizes]

    return render_template("/admin/quiz.html" , quizes = quiz_list)



@app.route("/admin/summary")
def admin_summary():

    return "admin summary"



@app.route("/admin/add_subject", methods= ["POST", "GET"])
def add_subject():
    if request.method == 'POST':
        subject_name = request.form['subject_name'].strip()
        description = request.form['description']

        if not subject_name:
            flash("Please Enter Subject Name...", "danger")
            return redirect(request.url)

        existing_subject = Subject.query.filter(Subject.name==subject_name).first()

        if existing_subject:
            flash("Subject Already Exits..." , "danger")
            return redirect(request.url)

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
        chapter_name = request.form['chapter_name'].strip()
        description = request.form['description']

        if not subject_id or not chapter_name:
            flash("Select Subject and Chapter...", "danger")
            return redirect(request.url)

        existing_chapter = Chapter.query.filter(Chapter.name==chapter_name, Chapter.subject_id==subject_id).first()

        if existing_chapter:
            flash("Chapter Already Exits" , "error")
            return redirect(request.url)
        
        new_chapter = Chapter(name = chapter_name, description = description, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        flash("Chapter Added Succeffully.." ,"success")
        return redirect(request.url) 
         
    return render_template("admin/chapter.html", add_chapter= True )



@app.route("/admin/edit-chapter", methods = ["POST", "GET"])
def edit_chapter():
    chapter_id = request.args.get('chapter_id')
    subject_id = request.args.get('subject_id')

    if request.method == "POST":
        chapter_name = request.form['chapter_name']
        description = request.form['description']

        if not chapter_id or not subject_id:
            flash("Something Went Wrong! Try Again...", "danger")
            return redirect(url_for("admin_dashboard"))

        if not chapter_name:
            flash("Chapter Name is required...", "danger")
            return redirect(request.url)
        
        chapter = db.session.query(Chapter).filter(Chapter.id == chapter_id).first()
        
        if chapter_name == chapter.name:
            chapter.description = description
            db.session.commit()
            flash("Chapter Edit Successfully..." , "success")
            return redirect(url_for('admin_dashboard'))
            

        existing_chapter = db.session.query(Chapter).filter(Chapter.name==chapter_name, Chapter.subject_id==subject_id).first()
        if existing_chapter:
            flash("Chapter Already Exists...", "danger")
            return redirect(request.url)

        chapter.name = chapter_name
        chapter.description = description
        db.session.commit()
        flash("Chapter Edit Successfully..." , "success")
        return redirect(url_for('admin_dashboard'))
    
    chapter_details = db.session.query(Chapter).filter(Chapter.id == chapter_id).first()

    return render_template("admin/chapter.html", chapter=chapter_details , edit_chapter=True)



@app.route("/admin/add-quiz", methods = ["POST", "GET"])
def add_quiz():
    if request.method == "POST":
        chapter_id = int(request.form['chapter'])
        date_of_quiz_str = request.form['date_of_quiz']
        time_duration = request.form['time']
        remarks = request.form['remarks']

        date_of_quiz = datetime.strptime(date_of_quiz_str, '%Y-%m-%d').date()

        if date_of_quiz < date.today():
            flash("Select a future date for quiz...")
            return redirect(request.url)

        if not chapter_id or not date_of_quiz or not time_duration:
            flash("Selct All Fields...", "danger")
            return redirect(request.url)

        new_quiz = Quiz(chapter_id = chapter_id, date_of_quiz = date_of_quiz, time_duration = time_duration, remarks = remarks)
        db.session.add(new_quiz)
        db.session.commit()
        flash("Quiz Added Successfully", "success")
        return redirect(request.url) 

    subjects = db.session.query(Subject).all()
    return render_template("/admin/quizform.html", subjects = subjects, add_quiz = True)



@app.route("/admin/edit-quiz", methods = ["POST", "GET"])
def edit_quiz():
    q = request.args.get("q")
    
    if request.method =='POST':
        chapter_id = request.form["chapter"]
        date_of_quiz_str = request.form['date_of_quiz']
        time_duration = request.form['time']
        remarks = request.form['remarks']

        date_of_quiz = datetime.strptime(date_of_quiz_str, '%Y-%m-%d').date()

        if date_of_quiz < date.today():
            flash("Select a future date for quiz...")
            return redirect(request.url)

        if not date_of_quiz or not time_duration or not chapter_id:
            flash("Fill All the Fields...", "danger")
            return redirect(request.url)
    

        quiz = db.session.query(Quiz).filter(Quiz.id == q ).first()

        if quiz.date_of_quiz < date.today():
            flash("Can't edit Previous quiz...", "danger")
            return redirect(request.url)

        quiz.chapter_id = chapter_id
        quiz.date_of_quiz = date_of_quiz
        quiz.time_duration = time_duration
        quiz.remarks = remarks
        db.session.commit()
        flash("Quiz Edited Successfully...", "success")
        return redirect(request.url)         

    if not q:
        return redirect(url_for("quiz"))

    quiz = db.session.query(
        Quiz.id.label("id"),
        Quiz.remarks.label("remarks"),
        Quiz.date_of_quiz.label("date_of_quiz"),
        Quiz.time_duration.label("time"),
        Quiz.chapter_id.label("chapter_id"),
        Chapter.name.label("chapter_name"),
        Quiz.remarks.label("remarks"),
        Subject.name.label("subject_name"))\
        .join(Quiz, Chapter.id == Quiz.chapter_id)\
        .join(Subject, Chapter.subject_id == Subject.id )\
        .filter(Quiz.id == q).first()
    
    subjects = db.session.query(Subject).all()

    return render_template("/admin/quizform.html",subjects = subjects,  quiz = quiz , edit_quiz = True)




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
            flash("All fields are required...", "error")
            return redirect(request.url)

        new_question = Question(quiz_id = quiz_id,chapter_id = chapter_id, question_statement = question_statement, option1 = option1, option2 = option2, option3 = option3, option4 = option4, correct_option = correct_option)
        db.session.add(new_question)
        db.session.commit()
        flash("Question Added Successfully...", "success")
        return redirect(request.url)
    
    return render_template("/admin/question.html", add_question = True)



@app.route("/admin/edit-question", methods = ["POST", "GET"])
def edit_question():
    question_id = request.args.get("id")

    if not question_id:
        flash("Something Went Wrong! Try Again..." , "danger")
        return redirect(url_for('quiz'))
    
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
        return redirect(url_for('quiz'))
    
    
    question = Question.query.filter_by(id=question_id).first()
    if not question:
        flash("Something Went Wrong! Try Again..." , "danger")
        return redirect(url_for('quiz'))
    
    return render_template("admin/question.html", question = question, edit_question = True)
    


@app.route("/admin/delete-chapter", methods = ["POST", "GET"])
def delete_chapter():
    chapter_id = request.args.get('id')
    if not chapter_id:
        flash("Chapter Deletion failed..." , "danger")
        return redirect(url_for('admin_dashboard'))
    
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    if not chapter:
        flash("chapter not Found..." , "danger")
        return redirect(url_for('admin_dashboard'))
    
    db.session.query(Question).filter(Question.chapter_id == chapter_id).delete()
    db.session.query(Quiz).filter(Quiz.chapter_id == chapter_id).delete()
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter Deleted Successfully...", "success")
    return redirect(url_for('admin_dashboard'))



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
        flash("Something Went Wrong! Try Again..." , "danger")
        return redirect(url_for('quiz'))
    
    question = Question.query.filter_by(id=question_id).first()
    if not question:
        flash("Something Went Wrong! Try Again..." , "danger")
        return redirect(url_for('quiz'))
    
    db.session.delete(question)
    db.session.commit()
    flash("Question Deleted Successfully.." , "success")
    return redirect(url_for('quiz'))





@app.route("/admin/delete-subject/<int:id>")
def dlt_subject(id):
    if id:
        exiting_subject = db.session.query(Subject).filter(Subject.id == id ).first()
        if not exiting_subject:
            flash("Subject not Exits..." "danger")
            return redirect(url_for("dashboard"))
    
        chapter = db.session.query(Chapter).filter(Chapter.subject_id == id).delete()






@app.route("/admin/search", methods = ["POST", "GET"])
def search():
    search = request.form["search"]

    subjects = db.session.query(Subject).filter(Subject.name.like(f"%{search}%")).all()
    users = db.session.query(User).filter(User.full_name.like(f"%{search}%")).all()
    quizes = db.session.query(Chapter).join(Quiz, Chapter.id == Quiz.chapter_id).filter(Chapter.name.like(f"%{search}%")).all()


    return render_template("admin/search.html", subjects= subjects, users= users, quizes = quizes)








def question_count(chapter_id):
        question_count = db.session.query(db.func.count(Question.id)) \
                        .filter(Question.chapter_id == chapter_id) \
                        .scalar()
        return question_count


def get_chapters(subject_id):
    query = db.session.query(Chapter) \
            .filter(Chapter.subject_id == subject_id).all()
    chapters = [{"id":chapter.id, "name": chapter.name, "questions_count": question_count(chapter.id)} for chapter in query]
    return chapters


def get_questions(quiz_id):
    query = db.session.query(Question)\
            .filter(Question.quiz_id == quiz_id)
    questions = [{"id": question.id ,"question_statement": question.question_statement } for question in query]
    return questions
    
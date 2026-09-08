# Quiz Master

A web-based quiz management and assessment platform built with **Flask, SQLite, SQLAlchemy, Flask-Login, Jinja2, and Matplotlib**.

Quiz Master allows administrators to manage subjects, chapters, quizzes, questions, and users, while registered users can participate in quizzes and track their scores and performance.

---

## Features

### 👨‍💼 Admin

* Secure admin authentication
* Create and manage subjects
* Create and manage chapters
* Create and manage quizzes
* Add, edit, and delete quiz questions
* Configure quiz duration and remarks
* Manage registered users
* View user performance
* View quiz scores and statistics
* Analyze quiz performance using graphical statistics

### 👨‍🎓 User

* User registration and login
* Secure session-based authentication
* User profile management
* Browse available subjects
* Browse chapters and quizzes
* Attempt quizzes
* Time-based quiz attempts
* Automatic score calculation
* View previous quiz results
* Track quiz performance
* View quiz statistics

---

## Tech Stack

| Technology           | Purpose                                    |
| -------------------- | ------------------------------------------ |
| **Python**           | Backend programming                        |
| **Flask**            | Web application framework                  |
| **Flask-SQLAlchemy** | Database ORM                               |
| **Flask-Login**      | User authentication and session management |
| **SQLite**           | Relational database                        |
| **Jinja2**           | Server-side HTML templating                |
| **HTML5**            | Frontend structure                         |
| **CSS3**             | Styling                                    |
| **JavaScript**       | Client-side interactions                   |
| **Matplotlib**       | Data visualization and statistics          |
| **Gunicorn**         | Production WSGI server                     |

The dependency versions are defined in the project's `requirements.txt`.

---

## Application Architecture

```text
                    ┌──────────────────────┐
                    │      Browser         │
                    │  HTML / CSS / JS     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Flask          │
                    │    Web Application    │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌────────────┐
       │   Admin    │   │    User    │   │    Auth    │
       │ Controllers│   │ Controllers│   │  & Session │
       └──────┬─────┘   └──────┬─────┘   └────────────┘
              │                │
              └────────┬───────┘
                       ▼
              ┌──────────────────┐
              │ Flask-SQLAlchemy │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │      SQLite      │
              │    Database      │
              └──────────────────┘
```

---

## Database Design

The application uses SQLite with SQLAlchemy models for managing users, subjects, chapters, quizzes, questions, and scores.

### Main Entities

```text
User
 │
 └── Score
       │
       └── Quiz
             │
             └── Question
             
Subject
 │
 └── Chapter
       │
       └── Quiz
```

### Models

#### User

Stores registered user information:

* Username
* Password
* Full name
* Qualification
* Date of birth

#### Subject

Represents a subject/category containing multiple chapters.

#### Chapter

Belongs to a subject and contains quizzes.

#### Quiz

Contains:

* Quiz date
* Time duration
* Remarks
* Questions
* User scores

#### Question

Contains:

* Question statement
* Four options
* Correct option

#### Score

Stores:

* User
* Quiz
* Attempt timestamp
* Total score

---

## Project Structure

```text
quiz_master_23f3003203/
│
├── controllers/
│   ├── admin_controller.py
│   ├── error_handler.py
│   ├── login_signup.py
│   └── user_controller.py
│
├── models/
│   └── model.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── ...
│
├── templates/
│   ├── admin/
│   ├── error/
│   ├── user/
│   ├── login.html
│   └── signup.html
│
├── instance/
│   └── quiz_master.db
│
├── app.py
├── requirements.txt
└── README.md
```

The repository currently separates controller logic, database models, static assets, and Jinja templates into dedicated directories.

---

## Quiz Workflow

```text
User Registration
       │
       ▼
     Login
       │
       ▼
Browse Subjects
       │
       ▼
Browse Chapters
       │
       ▼
Select Quiz
       │
       ▼
Attempt Questions
       │
       ▼
Submit Quiz
       │
       ▼
Calculate Score
       │
       ▼
Save Result
       │
       ▼
View Performance
```

---

## Admin Workflow

```text
Admin Login
    │
    ▼
Admin Dashboard
    │
    ├── Manage Users
    │
    ├── Manage Subjects
    │      │
    │      └── Manage Chapters
    │               │
    │               └── Manage Quizzes
    │                        │
    │                        └── Manage Questions
    │
    └── View Performance
```

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.10+
* pip
* Git

---

### 1. Clone the repository

```bash
git clone https://github.com/afzal-10-02/quiz_master_23f3003203.git
```

```bash
cd quiz_master_23f3003203
```

---

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the application

```bash
python app.py
```

The Flask application runs on:

```text
http://localhost:5000
```

The application is configured to run on port `5000`.

---

## Default Admin Account

The application initializes an administrator account during database setup.

For security, **do not use hardcoded credentials in a production deployment**. Change the credentials and move sensitive configuration into environment variables before deploying publicly.

---

## Authentication

Quiz Master uses **Flask-Login** for authentication and session management.

The application provides separate flows for:

* User login
* User registration
* Admin authentication
* Logout
* Protected routes

---

## Performance & Statistics

The application stores quiz attempts and scores in the database, allowing user performance to be analyzed over time.

**Matplotlib** is included in the project dependencies for generating data visualizations and statistical representations.

---

## Security Considerations

Before deploying this project to production, consider the following:

* Move the Flask secret key to environment variables.
* Never commit passwords or secrets to Git.
* Use strong production credentials.
* Disable Flask debug mode.
* Use HTTPS in production.
* Add CSRF protection for form submissions.
* Validate and sanitize user input.
* Use production-grade database configuration.
* Configure secure session cookies.

> **Note:** The current source contains a hardcoded Flask secret key and a default administrator password. These should be changed before production deployment.

---

## Future Improvements

Some possible improvements include:

* [ ] REST API for quiz operations
* [ ] JWT-based API authentication
* [ ] Password reset functionality
* [ ] Email notifications
* [ ] Question randomization
* [ ] Multiple question types
* [ ] Advanced analytics dashboard
* [ ] Leaderboard system
* [ ] Quiz categories and difficulty levels
* [ ] Export results to CSV/PDF
* [ ] Responsive UI improvements
* [ ] Docker support
* [ ] Automated testing
* [ ] CI/CD pipeline
* [ ] Production deployment

---

## Learning Outcomes

This project demonstrates practical experience with:

* Flask application development
* MVC-style project organization
* SQLAlchemy ORM
* Relational database design
* Authentication and session management
* CRUD operations
* Server-side rendering with Jinja2
* Form handling
* Quiz and assessment logic
* Data visualization
* Application deployment concepts

---

## License

This project is available for educational and development purposes.

---

## Author

**Afzal Jamal**

GitHub: [@afzal-10-02](https://github.com/afzal-10-02)

---

## Acknowledgements

Built as a learning project to practice **Python, Flask, SQLAlchemy, database design, authentication, and web application development**.

```

One important thing I noticed while checking the repo: **`.venv`, `__pycache__`, and the `instance` directory are currently visible in GitHub**. For a portfolio-quality repository, I strongly recommend adding these to `.gitignore` and removing them from Git tracking. Also, your `app.py` currently contains a hardcoded secret key and default admin password, so those should be changed before you showcase the repository publicly.

[Open your Quiz Master repository](https://github.com/afzal-10-02/quiz_master_23f3003203?utm_source=chatgpt.com)
```

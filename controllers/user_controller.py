from flask import Flask
from flask import render_template , request, redirect, url_for
from flask_login import login_required, logout_user, current_user
from flask import current_app as app


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_authenticated:
        return render_template("user/dashboard.html")
    
    return redirect(url_for("index"))

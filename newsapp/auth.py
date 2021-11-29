from flask import Blueprint,render_template,url_for,redirect,request,flash
from sqlalchemy.sql.functions import user
from app import db
from models import User
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash


auth = Blueprint("auth",__name__)



@auth.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash(f"Logged in as {user.username}!",category="success")
                login_user(user,remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password!",category="error")
        else:
            flash("Email doesnot exist!",category="error")
    return render_template("login.html",user=current_user)

@auth.route("/sign-up",methods=["POST","GET"])
def sign_up():
    
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email2")
        password1 = request.form.get("pass1")
        password2 = request.form.get("pass2")
        
        email_exist = User.query.filter_by(email=email).first()
        user_exist = User.query.filter_by(username=username).first()
        if email_exist:
            flash("Email is already in user!" , category="error")
        elif user_exist:
            flash("User is already registered!" , category="error")
        elif password1!=password2:
            flash(r"Password doesn't matched" , category="error")
        elif len(username) < 2:
            flash(r"Username is too short" , category="error")
        elif len(password1) < 6:
            flash(r"Password is too short" , category="error")
        else:
            new_user = User(email = email ,username = username ,password = generate_password_hash(password1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash(r"Account Created!" , category="success")
            return redirect(url_for("views.home"))

            
    
    return render_template("sign-up.html",user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

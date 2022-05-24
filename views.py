from operator import pos
from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from flask_login import login_required,current_user
from sqlalchemy.sql.functions import user
from .models import Post,User,Comments,Likes
from . import db
import requests

views = Blueprint("views",__name__)

@views.route("/")
@views.route("/home",methods=["POST","GET"])
@login_required
def home():
    username = User.query.all()
    posts = Post.query.all()
    return render_template("home.html" ,username=username, user=current_user ,posts=posts)

@views.route("/create-post",methods=["POST","GET"])
@login_required
def create_post():
    if request.method=="POST":
        title = request.form.get("title")
        text = request.form.get("post")
        if not text:
           flash("Post cannot be empty!",category="error") 
        else:
            post=Post(post=text,title=title,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post Created!",category="success")
            return redirect(url_for("views.home"))
            
    return render_template("create_post.html" , user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete(id):
    post = Post.query.filter_by(id=id).first()
    
    if not post:
        flash("Post Doesnot Exist!",category="error")
        
    elif current_user.id != post.author:
        flash("You dont have the permission to delete this post!",category="error")
        
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post Deleted!",category="success")


    
    return redirect(url_for("views.home"))

@views.route("/edit-post/<id>",methods=["POST","GET"])
@login_required
def edit(id):
    post = Post.query.filter_by(id=id).first()
    
    if not post:
        flash("Post Doesnot Exist!",category="error")
        
    elif current_user.id != post.author:
        flash("You dont have the permission to edit this post!",category="error")
        
    else:
        if request.method == "POST":
            title = request.form.get("title")
            text = request.form.get("post")
            post.title = title
            post.post = text
            db.session.commit()
            flash("Post Edited!",category="success")
            return redirect(url_for("views.home"))
        
    return render_template("edit_post.html" , user=current_user,post=post)
    

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    posts = user.posts
    
    if not user:
        flash("Such User dosenot exist!",category="error")
        return redirect(url_for("views.home"))
        
    return render_template("posts.html",posts=posts , user=current_user)



@views.route("/posts/news")
def news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=b63abbe2853c4e66bb49effe2da4e7fb"
    response = requests.get(url)
    data = response.json()
    articles = data["articles"]
    print(articles)
    return render_template("news.html",articles=articles,user=current_user)

    
@views.route("/create-comment/<post_id>",methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("comment")
    if not text:
        flash("Comment cannot be empty!",category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comments(text = text ,author = current_user.id,post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post Does not exists!",category="error")
            
    
    return redirect(url_for('views.home'))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()
    if not comment:
        flash("Comment does not exists!",category="error")
        
    elif current_user.id != comment.author and current_user.id!= comment.post.author:
        flash("You are not authorized to delete this comment!",category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment Deleted!",category="success")
            
    
    return redirect(url_for('views.home'))
    
@views.route("/like-post/<post_id>",methods=["POST"])
@login_required
def like(post_id):
    post = Post.query.filter_by(id = post_id).first()
    like = Likes.query.filter_by(author=current_user.id,post_id=post_id).first()
    
    if not post:
        return jsonify({"error":"Post doesnot exists"},400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Likes(author=current_user.id,post_id=post_id)
        db.session.add(like)
        db.session.commit()
    
    return jsonify({
        "likes" : len(post.likes),
        "liked" : current_user.id in map(lambda x :x.author,post.likes)
    })
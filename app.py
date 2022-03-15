"""Flask app for Auth"""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from sqlalchemy import false, update
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, Users, db, Feedback
from form import AddFeedback, FlaskForm, RegisterUser, LoginUser
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/', methods = ['GET'])
def home_page():
    """Redirect to /register"""
    
    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def show_register_form():
    """Show a form that when submitted will register/create a user"""
    
    if "username" in session:
        print(session['username'])
        return redirect(f"/users/{session['username']}")

    form = RegisterUser()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        new_user = Users.register(first_name = first_name, last_name = last_name, email = email,
                                    username = username, password = password)
        
        db.session.rollback()
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username

        flash(f"Added {first_name} to Database!")

        return redirect(f"/users/{session['username']}")

    else:
        return render_template('register_form.html', form = form)

@app.route('/users/<username>', methods = ['GET'])
def user_page(username):
    """Show User Page"""
    
    if "username" in session:
        current_user = Users.query.get(username)
        
        if current_user.username == session['username']:
        
            return render_template('user_page.html', current_user = current_user)
        else:
            raise Unauthorized()
        
    else: 
        flash('Please Register or Sign-in')
        return redirect('/')

@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):
    """Delete a User"""
    if "username" in session:
        username = Users.query.get(session['username'])
        
        if username.username == session['username']:
           
            
            db.session.delete(username)
            db.session.commit()
            session.clear()
            flash(f"Deletion Successful")
   
        return redirect("/")
    flash('Please Register or Sign-in')
    return render_template('/')

@app.route('/login', methods = ['GET', 'POST'])
def show_login_form():
    """Show a form that when submitted will login a user"""

    form = LoginUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        auth_user = Users.authenticate(username, password )
            
        if auth_user:
            session['username'] = auth_user.username
            print(session['username'])
            return redirect(f"/users/{session['username']}")
         
        else: 
            flash(f"Invalid Username/Password")
            return render_template('login_form.html', form = form)

    else:
        return render_template('login_form.html', form = form)

@app.route('/logout', methods = ['GET','POST'])
def logout_user():
    """Log a user out and redirect to home page"""

    session.clear()
    flash(f"Logout Successful")
    
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def show_feedback_form(username):
    """Show update-feedback form and process it."""
        
    if "username" in session:
        current_user = Users.query.get(username)
        
        if current_user.username == session['username']:
            
            
            form = AddFeedback()

            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data
                
                feedback = Feedback(title = title, content = content, username = username)

                db.session.rollback()
                db.session.add(feedback)
                db.session.commit()
                return redirect(f"/users/{session['username']}")

            return render_template('feedback_form.html', form = form, current_user = current_user)
        else:
            raise Unauthorized()

    return render_template('/register', methods = ['POST']) 

@app.route('/users/feedback/<feedback_id>/edit', methods = ['GET','POST'])
def edit_feedback(feedback_id):
    """Edit a piece of feedback"""

    if "username" in session:
        current_user = Users.query.get(session['username'])
        
        if current_user.username == session['username']:
           
            feedback = Feedback.query.get(feedback_id) 
            form = AddFeedback(obj = feedback)
                
            if form.validate_on_submit():
                feedback.title = form.title.data
                feedback.content = form.content.data

                db.session.commit()
                
                return redirect(f"/users/{session['username']}")
        else:
            raise Unauthorized()       
            
   
        return render_template('edit_feedback_form.html', feedback = feedback, form = form)
    flash('Please Register or Sign-in')
    return render_template('/')


@app.route('/feedback/<feedback_id>/delete', methods = ['POST'])
def delete_feedback(feedback_id):
    """Delete a piece of feedback"""
    if "username" in session:
        current_user = Users.query.get(session['username'])
        
        if current_user.username == session['username']:
           
            feedback = Feedback.query.get(feedback_id) 
           
            db.session.rollback()
            db.session.delete(feedback)
            db.session.commit()
                
   
        return redirect(f"/users/{session['username']}")
    flash('Please Register or Sign-in')
    return render_template('/')

 

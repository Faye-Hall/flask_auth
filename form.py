from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt


class RegisterUser(FlaskForm):
       
        first_name = StringField("First Name:", validators = [InputRequired()])
        
        last_name = StringField("Last Name:", validators = [InputRequired()])
        
        email = EmailField("Email:", validators = [InputRequired()])
        
        username = StringField("Username:", validators = [InputRequired()])
        
        password = PasswordField("Password:", validators = [InputRequired()])
        
    
class LoginUser(FlaskForm):
       
        username = StringField("Username:", validators = [InputRequired()])
        
        password = PasswordField("Password:", validators = [InputRequired()])
        
class AddFeedback(FlaskForm):
        
        title = StringField("Title:", validators = [InputRequired(), Length(max = 100)])
        content = TextAreaField("Feedback:", validators = [InputRequired()])
        
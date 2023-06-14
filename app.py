from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'seckey'

# Initialize the database
connect_db(app)

# Define the WTForms registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Register')

# Define the WTForms login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# Route: Redirect to /register
@app.route('/')
def redirect_to_register():
    return redirect('/register')

# Route: Show registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process form data and create a new user
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        # Create a new User object
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Add the new user to the database and commit the changes
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user_profile', username=username))
    return render_template('register.html', form=form)


# Route: Process login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Process form data and authenticate user
        username = form.username.data
        password = form.password.data
        
        # Query the user from the database
        user = User.query.filter_by(username=username).first()
        
        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            # Store the username in the session
            session['username'] = username
            return redirect(url_for('user_profile', username=username))

        
        # If the user does not exist or the password is incorrect,
        # display an error message
        flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)



# Route: Log out and clear session
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    
    return redirect('/')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('user_profile', username=session['username']))
        return f(*args, **kwargs)
    return decorated_function

# Route: Secret page
@app.route('/secret')
@login_required
def secret():
    # Check if the username is stored in the session
    if 'username' in session:
        return "You made it!"
    else:
        return redirect('/login')
    
# Route: User profile page
@app.route('/users/<username>')
def user_profile(username):
    # Check if the username is stored in the session
    if 'username' in session:
        # Query the user from the database
        user = User.query.filter_by(username=username).first()

        # Check if the user exists
        if user:
            # Render the user profile template and pass the user object
            return render_template('profile.html', user=user)

    # If the user is not logged in or the user does not exist, redirect to login
    return redirect('/login')

    
if __name__ == '__main__':
    app.run()

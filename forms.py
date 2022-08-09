"""Forms Model"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField
from wtforms.validators import InputRequired, Email, Length
# why need to install email_validator?


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username",
                            validators=[InputRequired(),
                            Length(max=20)])

    password = PasswordField("Password",
                            validators=[InputRequired(),
                            Length(max=100)])

    email = StringField("Email",
                        validators=[Email(),
                        Length(max=50)])

    first_name = StringField("First Name",
                            validators=[InputRequired(),
                            Length(max=30)])

    last_name = StringField("Last Name",
                            validators=[InputRequired(),
                            Length(max=30)])


class LoginForm(FlaskForm):
    """Form for logining in user."""

    username = StringField("Username",
                            validators=[InputRequired(),
                            Length(max=20)])

    password = PasswordField("Password",
                            validators=[InputRequired(),
                            Length(max=100)])
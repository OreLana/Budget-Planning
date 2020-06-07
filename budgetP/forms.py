from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, SelectField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from budgetP.models import User


class RegistrationForm(FlaskForm):
  firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
  lastname = StringField('Last Name', validators=[DataRequired()])
  username = StringField('User Name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is taken. Please choose a different one.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm): 
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class IncomeForm(FlaskForm):
  amount = IntegerField('Amount', validators=[DataRequired()])
  description = StringField('description', validators=[DataRequired()])
  income_type = SelectField('Income Type',[validators.input_required("Please choose an option")], choices=[('Salary','Salary'),('Investment','Investment'), ('Gift','Gift')])
  dismiss = SubmitField('Dismiss')
  submit = SubmitField('Submit')

class BudgetForm(FlaskForm):
  amount = IntegerField('Amount', validators=[DataRequired()])
  description = StringField('description', validators=[DataRequired()])
  expense = SelectField('Expense',[validators.input_required("Please choose an option")], choices=[('Feeding','Feeding'),('Clothing','Clothing'),('Transporation','Transportation'),
                                                                                                    ('Health','Health'),('Home','Home'),('Payments','Payments'),('Entertainment','Entertainment'),('Education','Education')])
  dismiss = SubmitField('Dismiss')
  submit = SubmitField('Submit')

class ExForm(FlaskForm):
  amount = IntegerField('Amount', validators=[DataRequired()])
  dismiss = SubmitField('Dismiss')
  submit = SubmitField('Submit')
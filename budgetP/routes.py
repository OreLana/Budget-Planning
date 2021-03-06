import os
import secrets
from PIL import Image
from flask import Flask, render_template, flash, redirect, url_for, request
from budgetP import app, db, bcrypt
from budgetP.forms import RegistrationForm, LoginForm, IncomeForm, BudgetForm, UpdateProfileForm
from budgetP.models import User, UserIncome, UserBudget
from flask_login import login_user, current_user, logout_user,login_required


@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html')

@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/register", methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('dashboard'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Your account has been created! You are now able to log in.', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

  def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
  form = UpdateProfileForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.firstname = form.firstname.data
    current_user.lastname = form.lastname.data
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated')
  elif request.method == 'GET':
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname
    form.username.data = current_user.username
    form.email.data = current_user.email
  image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
  return render_template('profile.html', title='Profile',
                           image_file=image_file, form=form)

@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('dashboard'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      return redirect(url_for('dashboard'))
    else:
        flash(f'Login unsuccessful. Please check email and password', 'danger')
  return render_template('login.html', title='Login', form=form)

@app.route("/dashboard")
@login_required
def dashboard():
  return render_template('dashboard.html')

@app.route("/dashboard/income", methods=['GET','POST'])
@login_required
def income():
  form = IncomeForm()
  if form.validate_on_submit():
    income = UserIncome(amount=form.amount.data, description=form.description.data, income_type=form.income_type.data, admin=current_user )
    UserBalance += int(form.amount.data)
    db.session.add(income)
    db.session.commit()
    flash('Your income has been added', 'success')
    return redirect(url_for('income'))
  return render_template('income.html', title='Add Income',
                           form=form, legend='Add Income')


@app.route("/dashboard/expense", methods=['GET','POST'])
@login_required
def expense():
  form = BudgetForm()
  if form.validate_on_submit():
    expense = UserBudget(amount=form.amount.data, description=form.description.data, expense=form.expense.data, admin=current_user)
    db.session.add(expense)
    db.session.commit()
    flash('Your expense has been added to your budget has been added', 'success')
    return redirect(url_for('expense'))
  return render_template('expense.html', title='Add expense',
                           form=form, legend='Add expense')


@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))

@app.route("/try")
def tryout():
  return render_template('try.html')
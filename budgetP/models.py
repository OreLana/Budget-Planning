from datetime import datetime
from budgetP import db, login_manager 
from flask_login import UserMixin 

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(20), unique=True, nullable=False)
  lastname = db.Column(db.String(20), unique=True, nullable=False)
  username = db.Column(db.String(20), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  incomes = db.relationship('UserIncome', backref='admin', lazy=True)
  

  def __repr__(self):
    return f"User('{self.firstname}','{self.lastname}','{self.username}','{self.email}'')"

class UserIncome(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  amount = db.Column(db.Integer(), nullable=False)
  description = db.Column(db.String(), nullable=False)
  income_type = db.Column(db.String(), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 
  def __repr__(self):
    return f"UserIncome('{self.amount}', '{self.description}','{self.income_type}')"

class UserBudget(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  amount = db.Column(db.Integer(), nullable=False)
  description = db.Column(db.String(), nullable=False)
  expense = db.Column(db.String(), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  

  def __repr__(self):
    return f"Post('{self.amount}', '{self.description}','{self.expense}')"
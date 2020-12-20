import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from Erros import *
import json


DATABASE_NAME = os.getenv("database_name", "trivia")
DATABASE_USER = os.getenv('DATABASE_USER', 'postgres')
DATABASE_PASS = os.getenv('DATABASE_PASS', 'postgres')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost:5432')
db_formate = "postgres://{}:{}@{}/{}"
database_path = db_formate.format(DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_NAME)
print(database_path)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# this is for creatig db entries
def new_question(body):
  try:
    return Question(question=body.get('question'),
                    answer=body.get('answer'),
                    category=int(body.get('category')) + 1,
                    difficulty=body.get('difficulty'))
  except:
    raise RequestFormateError


# this is for deleting

def delete_from_db(question_id):
  question = db.session.query(Question).filter(Question.id == question_id).first()
  db.session.delete(question)
  db.session.commit()

# this is method to add to the database
def add_to_db(obj):
  db.session.add(obj)
  db.session.commit()

# this function is for selecting the questions by category
def get_questions_by_category(category_id):
  # TODO fix the join error
  # questions = db.session.query(Question).join(Category).\
  #   filter(Question.category == Category.id,
  #           Category.type == category).all()
  # category_id = db.session.query(Category.id).filter(Category.type == category).first()
  questions = db.session.query(Question).filter(Question.category == category_id).all()
  return questions

# this function is for getting all categories
def get_all_categories():
  return Category.query.order_by(Category.id).all()

def get_all_questions():
  return Question.query.order_by(Question.id).all()

def get_question_like(body):
  term = body.get('searchTerm')
  category_id = body.get('currentCategory') + 1
  return db.session.query(Question).\
    filter(
      Question.category == category_id,
      Question.question.ilike("%{}%".format(term))
    ).all()
  
'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(Integer)
  difficulty = Column(Integer)

  # TODO fix the relationship error
  # category = db.relationship('Category', back_populates='question')

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  # TODO fix the realtionship error
  # question = db.relationship('Question', back_populates='category', lazy=True)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }
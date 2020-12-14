import os , random
from flask import Flask, request, abort, jsonify , send_file
from flask_sqlalchemy import SQLAlchemy
from Erros import *
from flask_cors import CORS
import random
from models import ( 
    setup_db, add_to_db , 
    get_questions_by_category , 
    get_all_categories, new_question , 
    delete_from_db , 
    get_all_questions,
    get_question_like
)


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # setting up the cors for all origins
  cors = CORS(app, resources = {r"/*":{"origins" : "*"}})

  #global variables
  OBJECTS_PER_PAGE = 10
  DEFAULT_CATEGORY = 1


  # defining the after_request to allow the Access-Control properties
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response

  # this route is a placeholder for the home
  @app.route('/', methods=['GET'])
  def home():
    return '<h1 style="text-align:center;font-family:Monaco;"> Hello </h1>'
    
  # this route to serve the requested svg files
  @app.route('/<string:name>.svg')
  def get_svg(name):
    try:
      return send_file('../templates/Art.svg', attachment_filename='Art.svg')
    except:
      abort(404)
  
  # this function is for serializing the objects returned from the database
  def serialize(arr):
    return list(map(lambda x : x.format(), arr))


  # helper function for paginating categories and questions
  def paginate_results(req,sel):
    page = req.args.get('page', 1, type=int)
    start = (page - 1) * OBJECTS_PER_PAGE
    end = start + OBJECTS_PER_PAGE

    objects = serialize(sel)
    return objects[start:end]


  # this end point returns all the available categories
  @app.route('/categories' , methods=['GET'])
  def get_categories():
    try:
      categories = get_all_categories()
      if not len(categories):
        abort(404)
      current_categories = paginate_results(request,categories)
      return jsonify({'categories' : current_categories})
    except:
      abort(500)

  # this is for displayinng the questions
  @app.route('/questions', methods=['GET'])
  def get_questions():
    try:
      category, questions, categories = '','',''
      try:
        category = request.args.get('category',DEFAULT_CATEGORY,type=str)
        questions = get_questions_by_category(category)
        categories = serialize(get_all_categories())
      except:
        abort(422)
      if not len(questions) or not len(categories):
        abort(404)
      questions_size = len(questions)
      questions = paginate_results(request,questions)
      return jsonify({
        'questions' : questions,
        'total_questions' : questions_size,
        'categories' : categories,
        'current_category' : category,
      })
    except:
      abort(500)


  '''
  @TODO: 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_category(category_id):
    try:
      questions = get_questions_by_category(category_id + 1)
      question_size = len(questions)
      print(question_size)
      questions = paginate_results(request, questions)
      return jsonify({
        'questions' : questions,
        'total_questions' : question_size,
        'current_category' : category_id,
      })
    except:
      abort(500)
    

  '''
  @TODO: 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      delete_from_db(question_id)
      return jsonify({
        'success' : True
      })
    except:
      abort(500)
    

  '''
  @TODO: 
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  def create_question(body):
    try:
      try:
        add_to_db(new_question(body))
      except RequestFormateError:
        abort(422)
      return jsonify({
        'success' : True
      })
    except:
      abort(500)
    

  '''
  @TODO:  
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def search_question():
    try:
      body = ''
      try:
        body = request.get_json()
        if(not 'searchTerm' in body):
          return create_question(body)
      except:
        abort(422)
      questions = serialize(get_question_like(body))
        
      return jsonify({
        'questions' : questions,
        'total_questions' : len(questions),
        'current_category' : body.get('currentCategory')
      })
    except:
      abort(500)

  '''
  @TODO
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def get_random_questions():
    try:
      body, category, pre_questions = '','',''
      try:
        body = request.get_json()
        category = body.get('quiz_category')
        pre_questions = body.get('previous_questions') 
      except:
        abort(422)
      questions = serialize(get_questions_by_category(int(category.get('id')) + 1) if category['type'] != 'click' else get_all_questions())
      random.shuffle(questions)
      result = None

      for question in questions:
        if int(question.get('id')) not in pre_questions:
          result = question
          break
      
      return jsonify({
        'question' : result,
      })
    except:
      abort(500)


  ''' 
  handlers for all expected errors 
  [404 , 422 , 500 ] 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success" : False,
      "status_code" : 404,
      "msg" : "the resource is not found"
    }) , 404

  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
      "success" : False,
      "status_code" : 400,
      "msg" : "the method is not allowed"
    }) , 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "status_code" : 422,
      "msg" : "the entry is not processable"
    }) , 422

  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "status_code" : 500,
      "msg" : "the server has some issues"
    }) , 500
  
  return app

    
# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.8.5

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To set up the environment:

```bash
source init_env.sh
```

To run the server:
```bash
make
```
or you could use your own commands.

``` 
Endpoints
    GET '/categories'
    GET '/questions'
    GET '/categories/<int:id>/questions'
    DELETE '/questions/<int:id>'
    POST '/questions'
    POST '/quizzes'


GET '/categories'
- Fetches a dictionary of categories in which there are the ids and the types of the categories
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a list a object of object each of the form id: category_id type:category_type. 
- Example: 
    [
    {"id" : "1", "type" : "Science"}, 
    {"id" : "2" , "type" : "Art"},
    {"id" : "3" : "type" : "Geography"},
    {"id ... }
    ]


GET '/questions'
- Fetches a dictionary of questions , categories , total number of questions , and current type of categories
- Request Argument: page which is an integer that spacifies the current page
- Returns: an object that has four fields 
    . questions: which is a list of objects that holds question info
    . total_questions: which is the number of the questions
    . categories: which all the available categories
    . current_category: which the category of the returned questions
- Example:
    [
        {
            "questions" : [{
                "question" : "this is a question",
                "answer" : "this is the answer",
                "category" : 1,
                "difficulty" : 2
            }, ...
            ],
            "total_questions" : 123,
            "category" : 1,
            "categories" : \\ the same as returned upbove ..

        }, ...
    ]


GET '/categories/<int:id>/questions'
- Fetches the a dictionary of questions of a spacific category
- URL variable:  is the number that represents the category.
- Request Argument: None
- Returns: an object with three fields 
    . questions: which is the required questions
    . total_questions: which is the total number of questions results.
    . current_category: which is the current category of the questions.
- Example:
    [
        {
            "questions" : [{
                "question" : "this is a question",
                "answer" : "this is the answer",
                "category" : 1,
                "difficulty" : 2
            }, ...
            ],
            "total_questions" : 123,
            "category" : 1
        }, ...
    ]


DELETE '/questions/<int:id>'
- Deletes the spacified question
- URL Variable: is the id of the question 
- Request Argument: None
- Returns: an object with one field
    . success: which is true or false
- Example:
    {
        "success" : True
    }


POST '/questions'
- The Action is dependent of the body
    - Creates a new Question if the body dosen't contain any SearchTerm
    - Request Argument: None
    - Request Body: must have the following fields
        . question: which holds the text of the question
        . answer: which is the answer text
        . difficulty: which is an integer that rate the question
        . category: which is an integer that references the category
    
    - Returns: an object with the same message as the DELETE
or
    - Searches for the Question that matches the SearchTerm provided in the body
    - Request Argument: None
    - Request Body: Must Contain the searchTerm field
    - Returns: an object with the same message as the DELETE


POST '/quizzes'
- Fetches a question at a time that belongs to a category
- Request Argument: None
- Request Body: must have the following fields
    . quiz_category: that is the integer that references the category of the quize
    . previous_questions: that is an array the holds the already shown questions
- Returns: an object that has one field which is question that holds the question info.
- Example:
    {
        "question":{
            "question" : "this is ...",
            "answer" : "this ...",
            ...
        }
    }

```


## Testing
To run the tests, run
```bash
make test
```
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.TEST_DB_NAME = os.getenv("TEST_DB_NAME","trivia")
        self.TEST_DB_USER = os.getenv('TEST_DB_USER', 'postgres')
        self.TEST_DB_PASS = os.getenv('TEST_DB_PASS', 'postgres')
        self.TEST_DB_HOST = os.getenv('TEST_DB_HOST', 'localhost:5432')
        self.database_path = "postgres://{}:{}@{}/{}".\
            format(self.TEST_DB_USER,self.TEST_DB_PASS,self.TEST_DB_HOST, self.TEST_DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.question = {
            "question" : "this is for testing",
            "answer" : "this is answer",
            "category" : "1",
            "difficulty" : "1"
        }

        self.bad_body = {
            "question" : "bad one"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    """
    def test_get_question(self):
        res = self.client().get('/categories/1/questions')
        data = res.get_json()
        self.assertEqual(res.status_code , 200)
        self.assertTrue(data['questions'])

    def test_create_question(self):
        res = self.client().post('/questions' , json=self.question)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'), True)

    def test_bad_request(self):
        res = self.client().post('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data.get('msg'), "the method is not allowed")

    def test_bad_body(self):
        res = self.client().post('/questions' , json=self.bad_body)
        data = res.get_json()

        self.assertTrue(res.status_code, 500)
        self.assertEqual(data.get("success"), False)
        self.assertEqual(data.get("msg"), "the server has some issues")
        




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
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
            "question": "this is for testing",
            "answer": "this is answer",
            "category": "1",
            "difficulty": "1"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    successful scenarios
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = res.get_json()
        res2 = self.client().get('/categories')
        categories = res2.get_json()['categories']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res2.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
        self.assertEqual(data['categories'], categories)

    def test_get_question(self):
        res = self.client().get('/categories/1/questions')
        data = res.get_json()

        self.assertEqual(res.status_code , 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertEqual(data['current_category'], 1)


    def test_create_question(self):
        res = self.client().post('/questions', json=self.question)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('id'))

    def test_delete_question(self):
        res2 = self.client().post('/questions', json=self.question)
        data2 = res2.get_json()
        added_id = data2['id']

        res = self.client().delete('/questions/{}'.format(added_id))
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data['id']), int(added_id))

    def test_search_question(self):
        search = {
            "searchTerm": "for testing",
            "currentCategory": 1
        }
        res = self.client().post('/questions', json=search)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['current_category'], 1)

    def test_get_quizzes(self):
        payload = {
            "previous_questions": [],
            "quiz_category":{
                "id": 1,
                "type": "Science"
            }
        }
        res = self.client().post('/quizzes', json=payload)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    """
    failure scenarios
    """
    def test_bad_request(self):
        res = self.client().post('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data.get('msg'), "the method is not allowed")


    def test_bad_body(self):
        res = self.client().post('/questions' , json={})
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data.get("success"), False)
        self.assertEqual(data.get("msg"), "the entry is not processable")
        
    def test_404_request(self):
        res = self.client().get('/categories/10000/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
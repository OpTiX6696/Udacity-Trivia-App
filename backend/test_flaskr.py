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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "password", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            'question': 'Who do  you think Ismail\'s best artiste is?',
            'answer': 'Brymo',
            'difficulty': 3,
            'category': '4'
        }
        
        self.get_next_quiz_question = {
            'previous_questions': [],
            'quiz_category': {
                'id': 0,
                'type': 'click'
            }
        }
        
        self.search_term = {
            'searchTerm': 'title'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_categories(self):
        """Successfully GET all categories"""
        
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        
        
    def test_405_get_categories_wrong_method(self):
        """Invalid Method for getting Categories (Uses post)"""
        
        res = self.client().post('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')
        
        
# ///////////////////////////////////////////
    def test_get_questions(self):
        """Successfully Get Questions On An Existant Page"""

        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

        
    def test_404_get_category_on_non_extant_page(self):
        """Invalid Page Number For Questions"""
        
        res = self.client().get('/questions?page=1000000')
        data = json.loads(res.data)
                
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

# ///////////////////////////////////////////

    def test_delete_question(self):
        """Successfully delete a question"""
        
        res = self.client().delete('/questions/6')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 6)
        
        
    def test_404_delete_non_extant_question(self):
        """Delete A Non Extant Question"""
        
        res = self.client().delete('/questions/100000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        
# ///////////////////////////////////////////

    def test_post_question(self):
        """Successfully Add A question"""
        
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_400_post_invalid_question(self):
        """Post An Empty Question Data or Search With an Empty Field"""
        
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
        self.assertEqual(data['error'], 400)
        
    def test_405_unallowed_method_to_add_question(self):
        """Post Question To The Wrong Endpoint"""
        
        res = self.client().post('questions/2', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')
        self.assertEqual(data['error'], 405)
        
        
    def test_search_question(self):
        """Successfully Search A Question"""
        
        res = self.client().post('/questions', json=self.search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

# ///////////////////////////////////////////

    def test_get_questions_by_category(self):
        """Successfully Get Questions By Category"""
        
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])
        
        
    def test_404_get_questions_by_invalid_category(self):
        """Get Questions By Invalid Category"""
        
        res = self.client().get('/categories/100000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Request')
        self.assertEqual(data['error'], 422)
        
# ///////////////////////////////////////////


    def test_get_next_question(self):
        """Successfully Get Next Question In Quiz"""
        
        res = self.client().post('/quizzes', json=self.get_next_quiz_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    
    def test_405_get_next_question_with_wrong_method(self):
        """Get Next Question In Quiz With A Wrong Method"""
        
        res = self.client().get('/quizzes', json=self.get_next_quiz_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')
        self.assertEqual(data['error'], 405)
    
        
        
        
# success': True,
#             'questions': paginated_questions,
#             'totalQuestions': len(questions),
#             'categories'


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
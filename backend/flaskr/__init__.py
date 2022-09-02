from crypt import methods
import os
# from ssl import AlertDescription
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """        
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,PATCH,DELETE,OPTIONS"
        )
        
        return response
    
    number_of_resources_per_page = 10

    def paginator(request, resources):
        page = request.args.get('page', 1, type=int)
        
        start = (page - 1) * number_of_resources_per_page
        end = start + number_of_resources_per_page
        
        f_resources = [res.format() for res in resources]
        paginated_resources = f_resources[start:end]
        
        return paginated_resources



    @app.route('/categories')
    def get_categories():
        """
        @TODO:
        Create an endpoint to handle GET requests
        for all available categories.
        """
        try:
            categories = Category.query.all()       
            f_categories = [category.format() for category in categories]
            dict_categories = { cat['id']: cat['type'] for cat in f_categories }

            return jsonify(
                {
                    'success': True,
                    'categories': dict_categories
                }
            )
        except:
            abort(404)
    

    @app.route('/questions')
    def get_questions():
        """
        @TODO:
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions.
        """
        
        try:
        
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.all()
            f_categories = [category.format() for category in categories]
            dict_categories = { cat['id']: cat['type'] for cat in f_categories }
            paginated_questions = paginator(request, questions)
            
            if not paginated_questions:
                abort(404)
        
        # print(dict_categories)
        # Category.query.get(questions['category'])['type']
        
        
            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'totalQuestions': len(questions),
                'categories': dict_categories,
                # 'currentCategory': 'History'
                
            })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            
            if question is None:
                abort(404)
            
            question.delete()
            
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route('/questions', methods=['POST'])
    def add_question():
        """Method to add question or search questions"""
        data = request.get_json()
        question = data.get('question')
        answer = data.get('answer')
        difficulty = data.get('difficulty')
        category = data.get('category')
        search_term = data.get('searchTerm')

        if search_term:
            try:
                if not search_term:
                    abort(400)
                
                search_results = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search_term))).all()
                f_results = [res.format() for res in search_results]
                
                categories = Category.query.all()
                f_categories = [category.format() for category in categories]
                dict_categories = { cat['id']: cat['type'] for cat in f_categories }
                
                return jsonify({
                    'success': True,
                    'questions': f_results,
                    'totalQuestions': len(search_results),
                    'categories': dict_categories,
                    # 'currentCategory': 'History'
                    
                })
            except:
                abort(422)
        else:       
        
            if (not question) or (not answer):
                abort(400)
            
            try:
                new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
                
                new_question.insert()
                
                # print (new_question.format())
                
                return jsonify({
                    'success': True,
                    'created': new_question.id
                })
            except:
                abort(422)
        

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """Successfully Get Questions By Category"""
        try:
            questions_by_category = Question.query.filter(Question.category == category_id).all()
            
            f_questions_by_category = [question.format() for question in questions_by_category]
            
            current_category = Category.query.get(category_id)
            
            return jsonify({
                'success': True,
                'questions': f_questions_by_category,
                'totalQuestions': len(questions_by_category),
                'currentCategory': current_category.type
            })
        except:
            abort(422)
    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        data = request.get_json()
        prev_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')
        try:
            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == quiz_category['id']).all()
        except:
            abort(422)
            
        eligible_next_questions = []
        
        for each in questions:
            if each.id not in prev_questions:
                eligible_next_questions.append(each)
            else:
                pass
        
        if not eligible_next_questions:
            abort(404)
            
        f_eligible_next_questions = [question.format() for question in eligible_next_questions]   
        
        next_question = random.choice(f_eligible_next_questions)
        
        prev_questions.append(next_question['id'])
        
        return jsonify({
            'success': True,
            'question': next_question
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    
    @app.errorhandler(404)
    def not_found(err):
        return (
            jsonify(
                {
                    'error': 404,
                    'success': False,
                    'message': 'Resource Not Found'
                }
            ), 404
        )
        
    @app.errorhandler(405)
    def invalid_method(err):
        return (
            jsonify(
                {
                    'error': 405,
                    'success': False,
                    'message': 'Method Not Allowed'
                }
            ), 405
        )
    
    @app.errorhandler(422)
    def unprocessable(err):
        return (
            jsonify(
                {
                    'error': 422,
                    'success': False,
                    'message': 'Unprocessable Request'
                }
            ), 422
        )
        
    @app.errorhandler(400)
    def bad_request(err):
        return (
            jsonify(
                {
                    'error': 400,
                    'success': False,
                    'message': 'Bad Request'
                }
            ), 400
        )






    return app


import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    question_range = questions[start:end]

    return question_range


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def get_categories():
        # Custom dict to hold looped query results
        all_categories = {}
        try:
            # Grab all categories
            select = Category.query.order_by(Category.id).all()

            # Add category to all_categories dict
            for category in select:
                all_categories[category.id] = category.type
        except:
            # Method not Allowed
            abort(405)
        return jsonify({
            "categories": all_categories,
            "success": True,
        })

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
    @app.route("/questions", methods=["GET"])
    def get_questions():
        all_categories = {}
        current_category = []

        try:
            #   Grab all questions and restrict to slice
            all_questions = Question.query.order_by(Question.id).all()
            paginated_questions = paginate(request, all_questions)

            # Grab Current Category
            questions_category = Question.query.with_entities(
                Question.category).order_by(Question.category).all()
            for question in questions_category:
                for q_category in question:
                    current_category.append(q_category)

            # Grab data for all categories
            select_categories = Category.query.order_by(Category.id).all()

            # add data to all_categories dict
            for category in select_categories:
                all_categories[category.id] = category.type
        except:
            abort(405)
        return jsonify({
            "questions": paginated_questions,
            "total_questions": len(all_questions),
            "categories": all_categories,
            "current_category": current_category,
            "success": True,
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        try:
            # Get question by Id and delete
            question = Question.query.get(id)
            question.delete()
        except:
            # Abort: Unprocessable if unable to delete
            abort(422)
        return jsonify({
            "success": True
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def post_question():
        try:
            # Get form data
            data = request.get_json()

            # Extract data
            question = data.get("question")
            answer = data.get("answer")
            category = data.get("category")
            difficulty = data.get("difficulty")

            # Make new question
            new_question = Question(
                question = question, 
                answer=answer, 
                category=category, 
                difficulty=difficulty
            )

            # Serialize Question
            new_question.insert()
        except:
            # Abort: Unprocessable if unable to save
            abort(422)
        return jsonify({
            "success": True,
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.


    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/find", methods=["POST"])
    def search_question():
        current_category = []
        try:
            # Get search term
            data = request.get_json()
            search_term = data.get("searchTerm")

            # Create substring to search for and Search
            sub_string = f'%{search_term}%'
            all_questions = Question.query.order_by(Question.category).filter(Question.question.ilike(sub_string)).all()
            paginated_questions = paginate(request, all_questions)

            # Grab Current Category
            questions_category = Question.query.with_entities(
                Question.category).order_by(Question.category).all()
            for question in questions_category:
                for q_category in question:
                    current_category.append(q_category)

        except:
            # Abort: Question not Found
            abort(404)
        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(paginated_questions),
            "current_category": current_category,
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:id>/questions")
    def get_questions_by_category(id):
        try:
            # Get questions by specified category id
            questions = Question.query.filter(Question.category == id)
            paginated_questions = paginate(request, questions)
        except:
            abort(405)
        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(paginated_questions),
            "current_category": id,
        })

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
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        # Get Quiz Params, if empty none
        data = request.get_json()
        previous_questions = data.get("previous_questions")
        category = data.get("quiz_category")

        try:
            # If Category is ALL, 
            if category['id'] == 0:
                questions = Question.query.order_by(Question.id).all()
            # If Category is Specific,
            elif (int(category['id']) in range(7)) and (int(category['id']) != 0):
                questions = Question.query.order_by(Question.id).filter(Question.category==int(category['id'])).all()
            # Select next batch of questions
            question_range = [question.format() for question in questions if question.id not in previous_questions]
            if len(question_range) == 0: 
                return jsonify({
                    'success': False,
                    'question': False
                    })
            return jsonify({
                    'success':True,
                    'question': random.choice(question_range) # Randomize Question Selection
                })
        except:
            abort(400)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "message": "bad request",
            "error": 400,
            "success": False
        }), 400
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "message": "Unprocessable",
            "error": 422,
            "success": False
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "message": "resource not found",
            "error": 404,
            "success": False
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "message": "internal server error",
            "error": 500,
            "success": False
        }), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "message": "method not allowed",
            "error": 405,
            "success": False
        }), 405

    return app

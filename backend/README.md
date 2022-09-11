# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Testing

To be able to run tests be sure to run the commands below

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation

### Getting Started

- Backend base URL: http://127.0.0.1:5000
- Frontend base URL: http://127.0.0.1:3000
- Authentication: There is no authentication or API keys equired for this version of the application.

### Error handling

Invoking any of the following errors will return a JSON object in this format:

```
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```

The API will return three error types when request fail:

- 400: Bad Request
- 405: Method Not Allowed
- 422: Not Processable
  {
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
  }

### Endpoints

**GET /categories**

- General:
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs, success value.
- Sample:`curl http://127.0.0.1:5000/categories`

```
{
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

**GET /questions**

- General:
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category and a list of the current category of each question and a dictionry of questions including answer, category, difficulty, id, question and total number of questions
  - Request Arguments: None
  - Returns: A list of questions, number of total questions, current category, categories and success value.
- Sample:`curl http://127.0.0.1:5000/questions`

```
{
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": [
    1,
    1,
    1,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
    5,
    5,
    5,
    5,
    6,
    6
  ],
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

**GET /categories/{category.id}/questions**

- General:
  - Fetches The current category id, a list of questions inside the category every question consists of a dictionry including answer, category, difficulty, id, question and total number of questions
  - Request Arguments: Category ID
  - Returns: A list of questions, number of total questions, current category and categories, success value.
- Sample:`curl http://127.0.0.1:5000/category/1/questions`

```
{
"current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

**DELETE /questions/{question.id}**

- General:
  - Deletes a certain question by a given ID if exists
  - Request Arguments: Question id
  - Returns: success value.
- Sample:`curl http://127.0.0.1:5000/questions/23 -X DELETE`

```
{
  "success": true
}
```

**POST /questions**

- General:
  - Creates a new question using the submitted question and answer text, difficulty and category score.
  - Request Arguments: question, answer, category, difficulty
  - Returns: success value.
- Sample:`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "What is the biggest pyramid?","answer": "The great pyramid", "category": 4, "difficulty": 2 }'`

```
{
  "success": true
}
```

**POST /questions/search**

- General:
  - Search for any question using the submitted search term which is a substring of the question.
  - Request Arguments: Search Term
  - Returns: current category, question, answer, category, difficulty, id, success value, total questions.
- Sample:`curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "pyramid"}'`

```
{
"current_category": [
    4
  ],
  "questions": [
    {
      "answer": "The great pyramid",
      "category": 4,
      "difficulty": 2,
      "id": 25,
      "question": "What is the biggest pyramid?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

**POST /quizzes**

- General:
  - Gets questions to play the quiz.
  - Request Arguments: Previous questions, Quiz category
  - Returns: success value, queestion, answer, category, difficulty, question id.
- Sample:`curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"id": 1, "type": "Science"}}'`

```
{
 "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}

```

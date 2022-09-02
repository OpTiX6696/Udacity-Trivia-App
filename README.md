# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.


# Documentation

This API serves quiz questions, categories, answers and other details that make it easy to develop a seamless gameplay in the frontend.

### Base URL

Since, I am running this on my local server, the base URL is:

**http://127.0.0.1:5000/**

### Get All Questions

This returns paginated questions with 10 questions per page, categories of the questions, total number of questions available and the success status of the request.

The *page* parameter is optional and defaults to 1, that is, the first page.

```bash
GET 'http://127.0.0.1:5000/questions?page=1'
```

Below is a sample response.

```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
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
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "totalQuestions": 14
}
```

### Get All Categories

This returns all quiz categories

```bash
GET 'http://127.0.0.1:5000/categories'
```

Below is a sample response.

```bash
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


### Delete A Question

This deletes a question with the id--*question_id* and returns the id of the deleted question and the success status.

```bash
DELETE 'http://127.0.0.1:5000/questions/question_id'
```

Below is a sample response.

```bash
{
  'success': True,
  'deleted': question_id
}
```


### Post A Question

```bash
POST 'http://127.0.0.1:5000/questions'
```

This adds a question with it's properties (answer, category and difficulty). This endpoint also ensures that empty object cannot be added to the database.
#### Sample Request Parameter

Below is a sample request body.

```bash
{
  'question': "Who do you think Ismail's best artiste is?",
  'answer': 'Brymo',
  'difficulty': 3,
  'category': 4
}
```
This returns the success status of the operation and the *id* of the question that has been added.
Below is a response example.

```bash
{
  'success': True,
  'created': id
}
```

### Search For A Question

```bash
POST 'http://127.0.0.1:5000//questions'
```

Search by any phrase. The questions list will update to include only questions that include the *searchTerm* within their question key.

#### Sample Request Parameter

Below is a sample request body.

```bash
{
  'searchTerm': 'title'
}
```

Below is a response example.

```bash
{
  'success': True,
  'questions': [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }],
  'totalQuestions': 20,
  'categories': {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }  
}
```


### Get Questions By Catgory

```bash
GET 'http://127.0.0.1:5000/categories/categoty_id/questions
'
```

This returns questions that belong to a given category. The *category_id* parameter in the URL represents the id of the particular category for which questions are to be returned.

The endpoint also returns the total number of questions under the category and that success status of the operation

Below is a sample response.

```bash
{
  "currentCategory": "History", 
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "totalQuestions": 2
}
```


### Playing the game

This endpoint takes category and previous question parameters and returns a random question within the given category, if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category, one question at a time is displayed, the user is allowed to answer and shown whether they were correct or not.

The game is set to five questions per session. So, after five questions, the game ends and displays the player's score.

However, if the chosen category has less than five questions, the game ends after the user has answered all the questions in that category.

```bash
POST 'http://127.0.0.1:5000/quizzes'
```

#### Sample Request Parameter

Below is a sample request body.

```bash
{
  'previous_questions': [],
  'quiz_category': {
      'id': 0,
      'type': 'click'
  }
}
```

Below is a sample response.

```bash
{
  'success': True,
  'question': {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }
}
```

The *question* is randomly chosen from a list of available questions that have not been displayed during a particular quiz session.


## Errors

Depending on the error, the response is formatted as shown below.

```bash
{
  'error': error_code,
  'success': False,
  'message': error_message
}
```

The **error_code** could be 400, 404, 405 or 422 depending on the error encountered.

The **error_message** is a string that corresponds with the **error_code**



# Thank you for coming this far. I hope you have a wonderful experience using this API











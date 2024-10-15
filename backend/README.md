
# Merit API

This project is a backend system for the **Merit** web application, which was built to aid students in their admission process into tetiary Institutions. 

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Additional Information](#additional-information)

## Project Overview

This project offers APIs to help students evaluate their scores for university admissions, determine whether they qualify for their chosen course, and get recommendations for other courses they might be eligible for based on their performance.

## Technologies Used

- Python (Flask)
- MySQL (Database)
- SQLAlchemy (ORM)
- Flask RESTful APIs
- HTML
- CSS
- JavaScript

## Installation

### Prerequisites

Before you can run the project, ensure that you have the following installed:

1. **Python 3.8+** - [Install Python](https://www.python.org/downloads/)
2. **Flask** - [Flask Installation](https://flask.palletsprojects.com/en/2.0.x/installation/)
3. **MySQL** - [Install MySQL](https://dev.mysql.com/downloads/)

### Step 1: Clone the Repository

```bash
git clone git clone https://github.com/your_username/Merit.git
cd Merit-backend-NG_version
```


### Step 2: Install Dependencies

Install all the required Python packages by running:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes the necessary dependencies for the project.

#### Key Packages:

- `Flask`: Web framework
- `SQLAlchemy`: ORM for database interaction
- `Flask-SQLAlchemy`: Extension for using SQLAlchemy with Flask
- `PyMySQL`: MySQL database connector

### Step 3: Running the Project

start the Flask development server:

```bash
# Export environment variables and run Flask
export FLASK_APP=views.py
flask run
```

This will start the server at `http://127.0.0.1:5000/`.

## API Endpoints

The backend exposes several endpoints that the frontend developers can interact with:

## GET /universities/courses
Retrieves a list of universities that offer a specific course. Accepts a query parameter `course_name` and returns a JSON object containing the course name and a list of universities offering the course.

**Query Parameters:**
- `course_name` (str, required): The name of the course to search for.

**Response Examples:**
- `200 OK`:
  ```json
    {
        "Universities offering the course": [
            "University of Ibadan (UI)",
            "University of Lagos (UNILAG)",
            "University of Nigeria, Nsukka (UNN)",
            "Obafemi Awolowo University (OAU)",
            "University of Benin (UNIBEN)"
        ],
        "course": "LAW"
    }

## POST, GET /evaluations/recommendations
Calculates and evaluates a student's eligibility for a specific course at a selected university. It also recommends other courses within the same faculty for which the student is qualified.

**Query Parameters:**
- `university_name` (str, required): The name of the university for which to retrieve the aggregate requirements. This must be passed as a query parameter.
- `course_name` (str, required): The name of the course to evaluate.
- `utme_score` (int, required): The student's UTME score.
- `post_utme_score` (int, required if applicable): The student's post-UTME score.
- `grades` (str, required if applicable): Comma-separated O-level grades (if required by the university).
- `no_of_sitting` (int, required if applicable): an integer greater than 0

**Response Examples:**
- `200 OK`:
  ```json
    {
        "University's name": "Obafemi Awolowo University (OAU)",
        "course": "ECONOMICS",
        "course aggregate": 70.38,
        "faculty": "SOCIAL SCIENCES",
        "other courses qualified for": {
            "BROADCAST JOURNALISM": 51.45,
            "DEMOGRAPHY AND SOCIAL STATISTICS": 53.75,
            "ENTREPRENEURSHIP": 52.53,
            "FILM PRODUCTION": 60.23,
            "GEOGRAPHY": 52.53,
            "INFORMATION SCIENCE AND MEDIA STUDIES": 50,
            "MASS COMMUNICATION": 71.05,
            "POLITICAL SCIENCE": 68.33,
            "PSYCHOLOGY": 63.83,
            "SOCIOLOGY": 51.3
        },
        "student's aggregate": 82.78,
        "university id": 4
    }

## GET /post-utme/requirements
Determines the required post-UTME score for a specific course at a selected university. Accepts a GET request with query parameters to calculate the required post-UTME score based on the student's UTME score and, if applicable, O-level grades.

**Query Parameters:**
- `university_name` (str, required): The name of the university for which to retrieve the aggregate requirements. This must be passed as a query parameter.
- `course_name` (str, required): The name of the course to evaluate.
- `utme_score` (int, required): The student's UTME score.
- `grades` (str, required if applicable): Comma-separated O-level grades (if required by the university).
- `no_of_sitting` (int, required if applicable): an integer greater than 0

**Response Examples:**
- `200 OK`:
  ```json
  {
      "course": "SOFTWARE ENGINEERING",
      "pass mark": 50.0,
      "post utme mark": 100,
      "required score": 63,
      "univeristy name": "Federal University of Technology, Akure (FUTA)",
      "university id": 7
  }


## GET /aggregates/requirements
Retrieves the required aggregate score for a specific course at a selected university. Accepts a GET request with a query parameter `course_name` to retrieve the required aggregate score for the specified course.

**Query Parameters:**
- `university_name` (str, required): The name of the university for which to retrieve the aggregate requirements. This must be passed as a query parameter.
- `course_name` (str, required): The name of the course to retrieve the aggregate score for.

**Response Examples:**
- `200 OK`:
  ```json
    {
        "course": "MICROBIOLOGY",
        "course aggregate": 66.25,
        "university id": 4,
        "university name": "Obafemi Awolowo University (OAU)"
    }

## GET /universities/description
Retrieves detailed information about a selected university. Accepts a GET request and returns detailed information about the selected university, including its name, ID, location, establishment year, and description.

**Query Parameters:**
- `university_name` (str, required): The name of the university for which to retrieve the aggregate requirements. This must be passed as a query parameter.

**Response Example:**
- `200 OK`:
  ```json
    {
        "Univerity name": "Obafemi Awolowo University (OAU)",
        "established": 1962,
        "location": "Ile-Ife, Nigeria",
        "university description": "Obafemi Awolowo University (OAU) is a comprehensive public institution located in Ile-Ife, Nigeria. Established in 1962, the university is named after Chief Obafemi Awolowo, a prominent Nigerian nationalist, statesman, and the first premier of the Western Region of Nigeria. OAU is renowned for its commitment to academic excellence, research, and community development. The university's sprawling campus is set on a vast expanse of land, providing a conducive environment for learning and research. OAU offers a wide range of undergraduate and postgraduate programs across various disciplines, contributing significantly to the intellectual and socio-economic development of Nigeria and beyond.",
        "university id": 4
    }


## GET /universities/list/courses
Retrieves a list of courses offered by a selected university. Accepts a GET request and returns a list of courses offered by the selected university, along with the university's name and ID.

**Query Parameters:**
- `university_name` (str, required): The name of the university for which to retrieve the aggregate requirements. This must be passed as a query parameter.

**Response Example:**
- `200 OK`:
  ```json
    {
        "List of courses": [
            "CREATIVE ARTS",
            "ENGLISH LANGUAGE",
            "FRENCH",
            "RUSSIAN",
            "HISTORY & STRATEGIC STUDIES",
            "LINGUISTICS /IGBO",
            "LINGUISTICS /YORUBA",
            "CHINESE",
            "LINGUISTICS",
            "PHILOSOPHY",
            "CHRISTIAN RELIGIOUS KNOWLEDGE",
            "ISLAMIC RELIGIOUS KNOWLEDGE",
            "DENTISTRY",
            "MEDICAL LABORATORY SCIENCE",
            "MEDICINE AND SURGERY",
            "NURSING SCIENCE",
            "PHARMACOLOGY",
            "PHYSIOLOGY",
            "PHYSIOTHERAPY",
            "...",
        ],
        "Univerity name": "University of Lagos (UNILAG)",
        "university id": 2
    }

## GET /course/faculty
Retrieves the faculty of a specific course at a selected university. Accepts a GET request with a query parameter `course_name` to retrieve the faculty to which the specified course belongs at the selected university.

**Query Parameters:**
- `university_name` (str, required): The name of the university for which to retrieve the aggregate requirements. This must be passed as a query  parameter.
- `course_name` (str, required): The name of the course to retrieve the faculty for.

**Response Examples:**
- `200 OK`:
  ```json
    {
        "course": "FRENCH",
        "faculty": "ARTS",
        "university id": 4,
        "university name": "Obafemi Awolowo University (OAU)"
    }


## GET /universities/faculties/courses
Retrieves a list of faculties and their respective courses offered by a selected university. Accepts a GET request and returns a list of faculties and the courses offered under each faculty at the selected university, along with the university's name and ID.

**Query Parameters:**
- `university_name` (str, required): The name of the university for which to retrieve the aggregate requirements. This must be passed as a query parameter.

**Response Example:**
- `200 OK`:
    ```json
  {
      "University name": "University of Ibadan (UI)",
      "faculties and their courses": {
          "AGRICULTURE": [
              "AGRICULTURAL ECONOMICS",
              "AGRICULTURAL EXTENSION AND RURAL DEVELOPMENT",
              "AGRONOMY",
              "ANIMAL SCIENCE",
              "AGRICULTURE (CPEB)"
          ],
          "ARTS": [
              "ARABIC LANGUAGE AND LITERATURE",
              "CLASSICAL STUDIES",
              "COMMUNICATION AND LANGUAGE ARTS",
              "ENGLISH LANGUAGE AND LITERATURE",
              "EUROPEAN STUDIES - FRENCH",
              "EUROPEAN STUDIES - GERMAN",
              "EUROPEAN STUDIES - RUSSIAN",
              "HISTORY",
              "IGBO",
              "ISLAMIC STUDIES",
              "LINGUISTICS",
              "MUSIC",
              "PHILOSOPHY",
              "RELIGIOUS STUDIES",
              "THEATRE ARTS",
              "YORUBA"
          ],
          "COLLEGE OF MEDICINE": [
              "BIOCHEMISTRY",
              "DENTISTRY",
              "ENVIRONMENTAL HEALTH SCIENCE",
              "HUMAN NUTRITION AND DIETETICS",
              "MEDICAL LABORATORY SCIENCE",
              "MEDICINE AND SURGERY",
              "NURSING SCIENCE",
              "PHYSIOLOGY",
              "PHYSIOTHERAPY"
          ]
          "...",
      },
      "university id": 1
  }


## GET /universities/list
Retrieves the list of supported universities.

This endpoint returns a list of universities currently supported by the application, filtered to include only those with available courses.

**Response Example:**
- `200 OK`:
    ```json
    {
        "Supported Universities": [
            "University of Ibadan (UI)",
            "University of Lagos (UNILAG)",
            "University of Nigeria, Nsukka (UNN)",
            "Obafemi Awolowo University (OAU)",
            "Federal University of Technology, Akure (FUTA)",
            "Nnamdi Azikiwe University (UNIZIK)",
            "University of Benin (UNIBEN)"
        ]
    }

## GET /universities/aggregate-requirements
Retrieves the aggregate requirements for admission into a specific university.

**Query Parameters:**
- `university_name` (str, required): The name of the university for which to retrieve the aggregate requirements. This must be passed as a query parameter.

**Response Examples:**
- `200 OK`:
  ```json
    {
        "aggregate requirements": {
            "aggr_year": "2022/2023",
            "max_jamb_score": 400,
            "max_post_utme": 40,
            "method": "utme_postutme_olevel",
            "olevel_subjects": 5,
            "postutme_passmark": 25,
            "require_olevel": true,
            "sitting": false,
            "university_id": 4,
            "university_name": "Obafemi Awolowo University (OAU)"
        }
    }

## GET /all/universities/courses
Retrieves all courses offered by all universities, along with the universities that offer each course.

**Response Examples:**
- `200 OK`:
  ```json
    {
        "courses": {
            "ACCOUNTANCY": [
            {
                "university_id": 3,
                "university_name": "University of Nigeria, Nsukka (UNN)"
            },
            {
                "university_id": 9,
                "university_name": "University of Benin (UNIBEN)"
            }
            ],
            "ACCOUNTANCY/ACCOUNTING": [
            {
                "university_id": 8,
                "university_name": "Nnamdi Azikiwe University (UNIZIK)"
            }
            ],
            ...
        }
    }


## GET /merit.ai
Renders the AI chatbot interface.

This endpoint serves the HTML page where users can interact with the AI chatbot. It accepts a GET request to load the chatbot UI.
**Response Examples:**
- `200 OK`:

The chatbot interface allowing users to enter queries and receive responses.


## POST /chat
Handles user input and provides AI chatbot responses.

This endpoint accepts user messages through a POST request, interacts with an AI model, and returns the chatbot's response. The conversation history is stored for reference.


## Additional Information

- **Frontend Integration**: The frontend can interact with the backend using JavaScript's `fetch()` or Axios for making HTTP requests to the Flask API.

If you have any questions or issues, feel free to contact the project maintainers.

Peter Ajimoti
email: oluwaseyipeter@gmail.com

## Remote MySQL Access

Currently, the MySQL database is set up locally, and external access is not available by default. 
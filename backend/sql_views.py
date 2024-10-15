from flask import Flask, render_template, request, jsonify, Response
from models import session as sql_session
from new_merit import uni_classes
from chat_model import history, model
from models import Universities
from flask_cors import CORS

from n_helper import (
    uni_dict, uni_classes, get_university_instance, universities)

app = Flask(__name__)

CORS(app)


@app.route('/universities/courses', methods=['GET'])
def get_universities_offering_course():
    """
    Returns a list of universities that offer a specific course.

    This endpoint accepts a GET request with a query parameter `course_name`
    and returns a JSON response containing a list of universities that offer
    the specified course.

    Query Parameters:
        course_name (str): The name of the course to search for.

    Returns:
        JSON response:
            - If the `course_name` parameter is missing, returns a 400 status
              code with an error message.
            - If no universities offer the specified course, returns a 404
              status code with a message.
            - Otherwise, returns a JSON object containing
              the course name and a list of universities offering the course.
    """
    course = request.args.get('course_name')
    if not course:
        return jsonify({"error": "course_name parameter is required"}), 400

    uni_list = []

    for CourseClass in uni_classes.values():

        _course = sql_session.query(CourseClass).filter(
            CourseClass.name == course).first()

        if _course:
            for uni in universities:
                if uni.id == _course.university_id:
                    uni_list.append(uni.name)

    if not uni_list:
        return jsonify({"message": "None of the supported"
                        f" universities offer {course}"}), 404

    result = {
        "course": course,
        "Universities offering the course": uni_list
    }
    return jsonify(result)


@app.route('/evaluations/recommendations', methods=['POST', 'GET'])
def calculate_evaluate_recommend():
    """
    Calculates and evaluates a student's eligibility for a specific course at
    a selected university.

    This endpoint accepts both POST and GET requests with query parameters to
    calculate the student's aggregate score and determine their eligibility for
    a specific course. It also recommends other courses within the same faculty
    for which the student is qualified.

    Query Parameters:
        course_name (str): The name of the course to evaluate.
        utme_score (int): The student's UTME score.
        post_utme_score (int): The student's post-UTME score.
        grades (str): Comma-separated O-level grades (if required).

    Returns:
        JSON response:
            - If any required parameter is missing, returns a 400 status code
            with an error message.
            - If the specified course is not offered at the
            selected university, returns a 404 status code with a message.
            - Otherwise, returns a JSON object containing
            the evaluation results, such as the course name, course aggregate,
            student's aggregate, university name, university ID, faculty, and
            other courses the student is qualified for.
    """
    result = get_university_instance(
        uni_dict, course=True, utme_score=True,
        post_utme_score=True, o_level=True, courses=True, sitting=True)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]
    uni = _class_instance.get_uni()
    courses = _class_instance.get_courses()
    utme_score = int(result["utme_score"])
    course = result["course"]
    uni_id = result["uni_id"]
    post_utme_score = result["post_utme_score"]
    o_level = result["o_level"]
    sitting = result["sitting"]

    if uni.aggr_method == "utme_postutme_olevel":
        if uni.sitting:
            stu_aggr = _class_instance.calculate_aggregate(
                utme_score, post_utme_score, o_level, sitting)
        else:
            stu_aggr = _class_instance.calculate_aggregate(
                utme_score, post_utme_score, o_level)

    if uni.aggr_method == "utme_olevel":
        if uni.sitting:
            stu_aggr = _class_instance.calculate_aggregate(
                utme_score, o_level, sitting)
        else:
            stu_aggr = _class_instance.calculate_aggregate(utme_score, o_level)

    if uni.aggr_method == "utme_postutme":
        stu_aggr = _class_instance.calculate_aggregate(
            utme_score, post_utme_score)

    course_aggr = _class_instance.get_course_aggregate(course)
    course_faculty = _class_instance.get_faculty(course)
    stu_aggr = round(stu_aggr, 2)

    same_faculty = [_course.name for _course in courses if _course.faculty ==
                    course_faculty and _course.name != course]

    qualified_to_study = {}

    if len(same_faculty) >= 1:
        qualified_to_study = {}
        for _course in courses:
            if _course.faculty == course_faculty:
                aggregate = _course.aggregate
                if aggregate:
                    if stu_aggr >= aggregate:
                        if _course.name != course:
                            qualified_to_study[_course.name] = aggregate

    result = {
        "course": course,
        "course aggregate": course_aggr,
        "student's aggregate": stu_aggr,
        "university name": result["selected_university"],
        "university id": uni_id,
        "faculty": course_faculty,
        "other courses qualified for": qualified_to_study
    }
    return jsonify(result)


@app.route('/post-utme/requirements', methods=['GET'])
def determine_required_post_utme_score():
    """
    Determines the required post-UTME score for a specific course at a selected
    university.

    This endpoint accepts a GET request with query parameters to calculate the
    required post-UTME score for a student based on their UTME score and, if
    applicable, O-level grades.

    Query Parameters:
        course_name (str): The name of the course to evaluate.
        utme_score (int): The student's UTME score.
        grades (str): Comma-separated O-level grades (if required).

    Returns:
        JSON response:
            - If any required parameter is missing, returns a 400 status code
            with an error message.
            - If the specified course is not offered at the selected
            university, returns a 404 status code with a message.
            - If the calculation is not supported at the selected university,
            returns a 404 status code with a message.
            - Otherwise, returns a with a JSON object containing
            the required post-UTME score, course name, post-UTME mark,
            pass mark, university name, and university ID.
    """
    result = get_university_instance(
        uni_dict, course=True, utme_score=True, o_level=True, courses=True)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]
    uni = _class_instance.get_uni()
    utme_score = int(result["utme_score"])
    course = result["course"]
    o_level = result["o_level"]

    course_aggr = _class_instance.get_course_aggregate(course)

    # for schools who don't use post utme
    if uni.aggr_method == "utme_olevel":
        return jsonify({
            "message": f"This feature is currently"
            f" unavailable for {result['selected_university']}."}), 404

    if uni.aggr_method == "utme_postutme_olevel":
        required_score = _class_instance.calculate_required_post_utme_score(
            course_aggr, utme_score, o_level)
    if uni.aggr_method == "utme_olevel":
        required_score = _class_instance.calculate_required_post_utme(
            course_aggr)
    if uni.aggr_method == "utme_postutme":
        required_score = _class_instance.calculate_required_post_utme_score(
            course_aggr, utme_score)

    if required_score is None:
        return jsonify({
            "message": "Currently not supported"
            f" at {result['selected_university']}."}), 404

    required_score = int(round(required_score))
    # make sure they get to the pass mark even if other grades are enough
    if required_score < uni.post_utme_passmark:
        required_score = uni.post_utme_passmark

    result = {
        "course": course,
        "required score": required_score,
        "post utme mark": uni.total_post_utme,
        "pass mark": uni.post_utme_passmark,
        "univeristy name": result["selected_university"],
        "university id": uni.id
    }

    return jsonify(result)


@app.route('/aggregates/requirements', methods=['GET'])
def get_required_aggregate():
    """
    Retrieves the required aggregate score for a specific course at a selected
    university.

    This endpoint accepts a GET request with a query parameter `course_name` to
    retrieve the required aggregate score for the specified course at the
    selected university.

    Query Parameters:
        course_name (str): The name of the course to retrieve the aggregate
        score for.

    Returns:
        JSON response:
            - If the `course_name` parameter is missing, returns a 400 status
            code with an error message.
            - If the course or its aggregate score is not found, returns a 404
            status code with an error message.
            - Otherwise, returns a  with a JSON object containing
            the course name, university name, university ID, and the required
            aggregate score for the course.
    """
    result = get_university_instance(uni_dict, course=True)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]

    course_aggr = _class_instance.get_course_aggregate(result["course"])
    if not course_aggr:
        return jsonify({"error": "course or course aggregate not found"}), 404

    result = {
        "course": result["course"],
        "university name": result["selected_university"],
        "university id": result["uni_id"],
        "course aggregate": course_aggr
    }
    return jsonify(result)


@app.route('/universities/description', methods=['GET'])
def about_university():
    """
    Retrieves detailed information about a selected university.

    This endpoint accepts a GET request and returns detailed information
    about the selected university, including its name, ID, location,
    establishment year, and description.

    Returns:
        JSON response:
            - A JSON object containing the university's name, ID, location,
            establishment year, and description.
    """
    result = get_university_instance(uni_dict)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]
    about = _class_instance.about_uni()
    if about:

        result = {
            "Univerity name": about.name,
            "university id": about.id,
            "location": about.location,
            "established": about.established,
            "university description": about.description
        }
        return jsonify(result)

    return None


@app.route('/universities/list/courses', methods=['GET'])
def display_list_of_courses():
    """
    Retrieves a list of courses offered by a selected university.

    This endpoint accepts a GET request and returns a list of courses offered
    by the selected university, along with the university's name and ID.

    Returns:
        JSON response:
            - A JSON object containing the university's name, ID, and a list
            of courses offered by the university.
    """
    result = get_university_instance(uni_dict)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]

    courses = _class_instance.get_courses()
    courses = [course.name for course in courses]
    courses = sorted(courses)

    result = {
        "Univerity name": result["selected_university"],
        "university id": result["uni_id"],
        "List of courses": courses
    }
    return jsonify(result)


@app.route('/course/faculty', methods=['GET'])
def get_faculty():
    """
    Retrieves the faculty of a specific course at a selected university.

    This endpoint accepts a GET request with a query parameter `course_name`
    to retrieve the faculty to which the specified course belongs at the
    selected university.

    Query Parameters:
        course_name (str): The name of the course to retrieve the faculty for.

    Returns:
        JSON response:
            - If the `course_name` parameter is missing, returns a 400 status
            code with an error message.
            - If the course or its faculty is not found, returns a 404 status
            code with an error message.
            - Otherwise, returns a 200 status code with a JSON object
            containing the university name, university ID, course name, and
            the faculty to which the course belongs.
    """
    result = get_university_instance(uni_dict, course=True)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]

    course = request.args.get('course_name')

    if not course:
        return jsonify({"error": "course_name parameter is required"}), 400

    faculty = _class_instance.get_faculty(course)

    if not faculty:
        return jsonify({"error": "course or faculty not found"}), 404

    result = {
        "university name": result["selected_university"],
        "university id": result["uni_id"],
        "course": result["course"],
        "faculty": faculty,
    }
    return jsonify(result)


@app.route('/universities/faculties/courses', methods=['GET'])
def display_faculties_and_courses():
    """
    Retrieves a list of faculties and their respective courses offered by a
    selected university.

    This endpoint accepts a GET request and returns a list of faculties and
    the courses offered under each faculty at the selected university, along
    with the university's name and ID.

    Returns:
        JSON response:
            - A JSON object containing the university's name, ID, and a
            dictionary where the keys are faculty names and the values are
            lists of courses offered by each faculty.
    """
    result = get_university_instance(uni_dict)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]
    faculties_data = _class_instance.get_faculties_and_courses()

    result = {
        "University name": result["selected_university"],
        "university id": result["uni_id"],
        "faculties and their courses": faculties_data
    }
    return jsonify(result)


@app.route("/universities/list")
def list_universities():
    """
    Retrieves the list of supported universities.

    This endpoint returns a list of universities currently
    supported by the application, filtered to include only those
    with available courses.

    Returns:
        JSON response:
            - A JSON object containing a list of university names
            that offer courses.
    """
    uni_list = []

    for uni in universities:
        if uni.uni_class:
            uni_list.append(uni.name)

    uni_list.sort()

    result = {
        "Supported Universities": uni_list
    }
    return jsonify(result)


@app.route("/all/universities/courses", methods=['GET'])
def get_all_courses_with_universities():
    """
    Returns a list of all courses along with the universities that offer them.

    This endpoint accepts a GET request and returns a JSON response containing
    each course and a list of universities (with names and IDs) that offer the
    course.

    Returns:
        JSON response:
            - If no universities or courses are found, returns a 404 status
              code with a message.
            - Otherwise, returns a 200 status code with a JSON object
              containing each course and the universities offering it.
    """
    courses_with_universities = {}

    for CourseClass in uni_classes.values():

        courses = sql_session.query(CourseClass, Universities.name).join(
            Universities, CourseClass.university_id == Universities.id).all()

        if courses:
            for course, university_name in courses:
                course_name = course.name
                university_info = {
                    "university_name": university_name,
                    "university_id": course.university_id
                }

                if course_name not in courses_with_universities:
                    courses_with_universities[course_name] = []
                courses_with_universities[course_name].append(university_info)

    if not courses_with_universities:
        return jsonify({"message": "No courses or universities found"}), 404

    result = {
        "courses": courses_with_universities
    }

    return jsonify(result)


@app.route("/universities/aggregate-requirements", methods=['GET'])
def get_aggregate_requirements():
    """
    Retrieve aggregate requirements for universities.

    This endpoint fetches and returns the aggregate requirements for
    a specific university.

    Returns:
        Response: A JSON response containing the aggregate requirements.
        If the requirements are not available, it returns None.
    """
    result = get_university_instance(uni_dict)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]

    requirment_dict = _class_instance.get_aggregate_docs()

    if not requirment_dict:
        return None
    result = {
        "aggregate requirements": requirment_dict
    }
    return jsonify(result)


# AI chatbot


@app.route("/merit.ai", methods=['GET'])
def home():
    """
    Renders the AI chatbot interface.

    This endpoint serves the HTML page where users can interact with the AI
    chatbot. It accepts a GET request to load the chatbot UI.

    Returns:
        HTML page:
            - The chatbot interface allowing users to enter queries and
            receive responses.
    """
    return render_template('chatbot.html')


@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles user input and provides AI chatbot responses.

    This endpoint accepts user messages through a POST request,
    interacts with an AI model, and returns the chatbot's response.
    THe conversation history is stored for reference.

    JSON request body:
        - "message" (str): The user input to be processed by the AI chatbot.

    JSON response:
        - A JSON object containing the AI model's response.
    """
    user_input = request.json.get("message", "")

    chat_session = model.start_chat(
        history=history
    )

    response = chat_session.send_message(user_input)
    model_response = response.text

    # Save the conversation in history
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})

    return jsonify({"response": model_response})


if __name__ == '__main__':
    app.run(debug=True)

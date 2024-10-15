from flask import Flask, render_template, request, jsonify, Response
from universities import universities
from flask_cors import CORS
from chat_model import history, model

from helper import (
    uni_dict,
    not_support_post_utme,
    utme_olevel,
    sittings,
    utme_postutme,
    utme_postutme_olevel,
    get_university_instance
)

app = Flask(__name__)

# Enable CORS for all routes
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
    for uni in universities:
        if uni["courses"] is not None:
            if course in uni["courses"].keys():
                uni_list.append(uni["name"])

    if not uni_list:
        return jsonify({"message": f"No universities offer {course}"}), 404

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
        uni_dict, course=True, utme_score=True, post_utme_score=True,
        o_level=True, courses=True, sitting=True)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]
    utme_score = int(result["utme_score"])
    course = result["course"]
    uni_id = result["uni_id"]
    post_utme_score = result["post_utme_score"]
    o_level = result["o_level"]
    sitting = result["sitting"]

    # get student aggregate and course aggregate
    course_aggr = _class_instance.get_course_aggregate(course)
    if uni_id in utme_postutme_olevel:
        if uni_id in sittings:
            stu_aggr = _class_instance.calculate_aggregate(
                utme_score, post_utme_score, o_level, sitting)
        else:
            stu_aggr = _class_instance.calculate_aggregate(
                utme_score, post_utme_score, o_level)

    elif uni_id in utme_olevel:
        if uni_id in sittings:
            stu_aggr = _class_instance.calculate_aggregate(
                utme_score, o_level, sitting)
        else:
            stu_aggr = _class_instance.calculate_aggregate(utme_score, o_level)

    else:
        stu_aggr = _class_instance.calculate_aggregate(
            utme_score, post_utme_score)
    stu_aggr = round(stu_aggr, 2)

    course_faculty = _class_instance.get_faculty(course)

    same_faculty = []
    courses_data = _class_instance.get_courses().items()

    for _course, details in courses_data:
        if course_faculty == details["faculty"]:
            if _course != course:
                same_faculty.append(details["faculty"])

    qualified_to_study = {}

    """create a dictionary that contains all
    the courses a user is qualifies to study"""
    if len(same_faculty) >= 1:
        qualified_to_study = {}
        for _course, course_details in courses_data:
            if course_faculty == course_details["faculty"]:
                aggregate = course_details["aggregate"]
                if aggregate:
                    if stu_aggr >= aggregate:
                        if _course != course:
                            qualified_to_study[_course] = aggregate
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
    required post-UTME score for a student based on their pUTME score and, if
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
    utme_score = int(result["utme_score"])
    course = result["course"]
    uni_id = result["uni_id"]
    o_level = result["o_level"]

    index = uni_id - 1

    post_utme_mark = _class_instance.universities[index]["total post utme"]

    course_aggr = _class_instance.get_course_aggregate(course)

    if uni_id in not_support_post_utme:
        return jsonify({
            "message": "This feature is currently unavailable"
            f"for {result['selected_university']}."}), 404

    if uni_id in utme_postutme_olevel:
        required_score = _class_instance.calculate_required_post_utme_score(
            course_aggr, utme_score, o_level)
    elif uni_id in utme_olevel:
        required_score = _class_instance.calculate_required_post_utme(
            course_aggr)
    else:
        required_score = _class_instance.calculate_required_post_utme_score(
            course_aggr, utme_score)

    if required_score is None:
        return jsonify({
            "message": "Currently not supported"
            f"at {result['selected_university']}."}), 404

    required_score = int(round(required_score))
    postutme_passmark = _class_instance.get_aggregate_docs()[
        "postutme_passmark"]
    if required_score < postutme_passmark:
        required_score = postutme_passmark

    result = {
        "course": course,
        "required score": required_score,
        "post utme mark": post_utme_mark,
        "postutme_passmark": postutme_passmark,
        "univeristy name": result["selected_university"],
        "university id": uni_id
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
    about_uni = _class_instance.about_uni()

    if about_uni:

        result = {
            "Univerity name": result["selected_university"],
            "university id": result["uni_id"],
            "location": about_uni["location"],
            "established": about_uni["established"],
            "university description": about_uni["description"]
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

    courses = list(_class_instance.get_courses().keys())
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
    # selected_university = "Obafemi Awolowo University (OAU)"
    result = get_university_instance(uni_dict, course=True)

    if isinstance(result, tuple) and isinstance(result[0], Response):
        return result

    _class_instance = result["class_instance"]
    faculty = _class_instance.get_faculty(result["course"])

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
    uni_list = sorted([uni.get("name") for uni in universities if uni.get(
        "courses") and uni.get("name")])

    uni_list.sort()

    result = {
        "Supported Universities": uni_list
    }

    return jsonify(result)


@app.route("/all/universities/courses", methods=['GET'])
def get_all_universities_and_courses():
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

    for uni in universities:
        if uni["courses"]:
            for course_name in uni["courses"].keys():
                university_info = {
                    "university_name": uni["name"],
                    "university_id": uni["id"]
                }
                # If the course is not already in the dictionary, add it
                if course_name not in courses_with_universities:
                    courses_with_universities[course_name] = []
                # Append the university info to the list for the course
                courses_with_universities[course_name].append(university_info)

    if not courses_with_universities:
        return jsonify(
            {"message": "No courses available across the universities."}), 404

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

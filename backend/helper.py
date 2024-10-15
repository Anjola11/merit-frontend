"""A helper file"""
from unilogics.uniben import Uniben
from unilogics.unizik import Unizik
from unilogics.futa import Futa
from unilogics.unn import Unn
from unilogics.unilag import Unilag
from unilogics.oau import Oau
from unilogics.ui import Ui
from universities import universities
from flask import jsonify, request
from docs_required import sittings


uni_dict = {uni['name']: uni['id'] for uni in universities}

# supported universities


def check_uni(uni_id):
    supported_uni = [1, 2, 3, 4, 7, 8, 9]
    uni_id = int(uni_id)
    if uni_id not in supported_uni:
        return False


# these school does not support post utme
not_support_post_utme = [3]


# group universities with their id according -
# - to their style of aggregate calculation
utme_postutme = [1, 7, 8, 9]
utme_postutme_olevel = [2, 4]
utme_olevel = [3]

grades_needed = {
    2: 5,
    3: 4,
    4: 5
}

# for views.py
uni_classes = {
    "1": Ui,
    "2": Unilag,
    "3": Unn,
    "4": Oau,
    "7": Futa,
    "8": Unizik,
    "9": Uniben,
}

# creates a class instance


def create_class_instance(uni_id):
    uni_id_str = str(uni_id)
    _class = uni_classes[uni_id_str]
    _class_instance = _class(uni_id)
    return _class_instance


def get_university_instance(uni_dict, course=None, utme_score=None,
                            post_utme_score=None, o_level=None,
                            courses=None, sitting=None):
    """Fetch university instance based on the provided university name."""
    course_ = None
    utme_score_ = None
    post_utme_score_ = None
    o_level_ = None
    courses_ = None
    sitting_ = None

    selected_university = request.args.get('university_name')

    if not selected_university:
        return jsonify({"error": "university_name parameter is missing"}), 400

    uni_id = uni_dict.get(selected_university)

    if uni_id is None:  # Check if the university ID is found
        return jsonify({"error": "university not found"}), 404

    if check_uni(uni_id) is False:
        return jsonify({"error": "university currently not supported"}), 404

    # Create class instance
    _class_instance = create_class_instance(uni_id)

    if course:
        course_ = request.args.get('course_name')
        if not course_:
            return jsonify({"error": "course_name parameter is required"}), 400
    if utme_score:
        utme_score_ = request.args.get('utme_score')
        if not utme_score_:
            return jsonify({"error": "utme_score parameter is required"}), 400

    if post_utme_score:
        index = uni_id - 1
        post_utme_score_ = None
        if uni_id not in not_support_post_utme:
            post_utme_score_ = request.args.get('post_utme_score')
            if not post_utme_score_:
                return jsonify(
                    {"error": "post_utme_score parameter is required"}), 400

        if post_utme_score_:
            post_utme_score_ = int(post_utme_score_)
            max_post_utme = universities[index].get("total post utme")
            if post_utme_score_ > max_post_utme:
                return jsonify({"error": f"Max score is {max_post_utme}"}), 400
    if o_level:
        if uni_id in utme_postutme_olevel or uni_id in utme_olevel:
            o_level_ = request.args.get('grades')
            if o_level_:
                o_level_grades = o_level_.split(',')
                no_of_grades = grades_needed[uni_id]
                if len(o_level_grades) != no_of_grades:
                    return jsonify(
                        {"error": f"Enter {no_of_grades} grades."}), 400
            else:
                return jsonify({"error": "grades parameter is required"}), 400
    if sitting:
        if uni_id in sittings:
            sitting_ = request.args.get('no_of_sitting')
            if not sitting_:
                return jsonify(
                    {"error": "no_of_sitting parameter is required"}), 400
            if not sitting_.isdecimal():
                return jsonify(
                    {"error": "no_of_sitting must be an integer"}), 400
            if sitting_.isdecimal() and int(sitting_) <= 0:
                return jsonify(
                    {"error": "no_of_sitting must be greater than 0"}), 400

            sitting_ = int(sitting_)

    if courses and course:
        courses_ = list(_class_instance.get_courses().keys())
        if course_ not in courses_:
            return jsonify({
                "message": f"The course '{course_}' is not offered at"
                f"{selected_university}. Please select another course."
            }), 404

    return {
        "selected_university": selected_university,
        "uni_id": uni_id,
        "class_instance": _class_instance,
        "course": course_,
        "utme_score": utme_score_,
        "post_utme_score": post_utme_score_,
        "o_level": o_level_,
        "sitting": sitting_
    }

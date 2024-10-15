from n_unilogics.uniben import Uniben
from n_unilogics.unizik import Unizik
from n_unilogics.futa import Futa
from n_unilogics.unn import Unn
from n_unilogics.unilag import Unilag
from n_unilogics.oau import Oau
from n_unilogics.ui import Ui

from models import Universities, session

from flask import jsonify, request

from models import (
    Universities,
    About,
    UiCourses,
    UnilagCourses,
    UnnCourses,
    OauCourses,
    AbuCourses,
    UnilorinCourses,
    FutaCourses,
    UnizikCourses,
    UnibenCourses,
    FuoyeCourses
)

# maps university names with their mysql classes
uni_classes = {
    "University of Ibadan": UiCourses,
    "University of Lagos": UnilagCourses,
    "University of Nigeria": UnnCourses,
    "Obafemi Awolowo University": OauCourses,
    "Federal University of Technology Akure": FutaCourses,
    "Nnamdi Azikiwe University": UnizikCourses,
    "University of Benin": UnibenCourses,
}

universities = session.query(Universities).all()
# maps universities names and id's
uni_dict = {uni.name: uni.id for uni in universities}

# maps university classes with their id's
uni_classes_logics = {
    "1": Ui,
    "2": Unilag,
    "3": Unn,
    "4": Oau,
    "7": Futa,
    "8": Unizik,
    "9": Uniben,
}


def create_class_instance(uni_id):
    uni_id_str = str(uni_id)
    _class = uni_classes_logics[uni_id_str]
    _class_instance = _class(uni_id)
    return _class_instance


def check_uni(uni_id):
    for uni in universities:
        if uni.id == uni_id:
            if uni.uni_class is None:
                return False


def get_university_instance(uni_dict, course=None, utme_score=None,
                            post_utme_score=None, o_level=None,
                            courses=None, sitting=None):
    """Fetch university instance based on the provided university name."""
    course_ = None
    utme_score_ = None
    post_utme_score_ = None
    o_level_ = None
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
    uni = _class_instance.get_uni()
    uni_id = uni.id

    if course:
        course_ = request.args.get('course_name')
        if not course_:
            return jsonify({"error": "course_name parameter is required"}), 400
    if utme_score:
        utme_score_ = request.args.get('utme_score')
        if not utme_score_:
            return jsonify({"error": "utme_score parameter is required"}), 400

    if post_utme_score:
        post_utme_score_ = None
        if uni.aggr_method != "utme_olevel":
            post_utme_score_ = request.args.get('post_utme_score')
            if not post_utme_score_:
                return jsonify(
                    {"error": "post_utme_score parameter is required"}), 400

        if post_utme_score_:
            post_utme_score_ = int(post_utme_score_)
            total_post_utme = uni.total_post_utme
            if post_utme_score_ > uni.total_post_utme:
                return jsonify(
                    {"error": f"Max score is {total_post_utme}"}), 400
    if o_level:
        if uni.aggr_method != "utme_postutme":
            o_level_ = request.args.get('grades')
            if o_level_:
                o_level_grades = o_level_.split(',')
                if len(o_level_grades) != uni.olevel_subjects:
                    return jsonify(
                        {"error": f"Enter {uni.olevel_subjects} grades."}), 400
            else:
                return jsonify({"error": "grades parameter is required"}), 400
    if sitting:
        if uni.sitting:
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
        courses_ = _class_instance.get_courses()
        course_names = [_course.name for _course in courses_]

        if course_ not in course_names:
            return jsonify({
                "message": f"The course '{course_}' is not offered at"
                "{selected_university}. Please select another course."
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

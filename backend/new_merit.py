"""Defines a class University"""
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
from models import Universities, About, session
import sys
from collections import defaultdict

MAX_JAMB_SCORE = 400


# Mapping of university IDs to course classes
university_courses_map = {
    1: UiCourses,
    2: UnilagCourses,
    3: UnnCourses,
    4: OauCourses,
    5: AbuCourses,
    6: UnilorinCourses,
    7: FutaCourses,
    8: UnizikCourses,
    9: UnibenCourses,
    10: FuoyeCourses
}

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


class University:
    universities = session.query(Universities).all()
    """Initializes a university with an id."""

    def __init__(self, id):
        self.id = id

    def get_uni(self):
        """Gets a university and related info"""
        uni_id = self.get_uni_index()
        uni = session.query(Universities).filter_by(id=uni_id).first()
        return uni

    def display_universities(self):
        """Displays all universities."""
        for uni in self.universities:
            print("{}. {}".format(uni.id, uni.name))

    def get_uni_index(self):
        """Get's the index of a particular
        university in the universities list."""
        for uni in self.universities:
            if uni.id == self.id:
                uni_index = uni.id
                self.uni_index = uni_index
                return uni_index

    def get_courses(self):
        """Fetches all the courses for a selected university from the database.
        """
        uni_id = self.get_uni_index()
        course_class = university_courses_map.get(uni_id)
        courses = session.query(course_class).filter_by(
            university_id=uni_id).all()
        if courses:
            return courses
        return None

    def get_faculty(self, course):
        """Returns the faculty of a given course"""
        courses = self.get_courses()
        for _course in courses:
            if course == _course.name:
                return _course.faculty
        return None

    def get_course_aggregate(self, _course):
        """Get the aggregate score of a selected course using MySQL."""
        courses = self.get_courses()

        if not courses:
            return None

        for course in courses:
            if course.name == _course:
                return course.aggregate

        return None

    def list_courses(self):
        """Lists out all the courses offered in a selected university."""
        uni = self.get_uni()
        print("List of Courses offered in {}".format(uni.name))
        phrase_len = len(uni.name) + len("List of Courses offered in ")
        print("=" * phrase_len)
        courses = self.get_courses()
        for course in courses:
            print("{}. {}".format(course.id, course.name))

    def get_faculties_and_courses(self):
        """Fetches all the faculties and courses under
        them for the selected university."""
        courses = self.get_courses()

        if courses:
            faculty_courses = defaultdict(list)
            for course in courses:
                faculty_courses[course.faculty].append(course.name)
            return dict(faculty_courses)
        else:
            return None

    def get_aggregate_docs(self):
        """Gets the aggregate requirment for a specific university"""
        uni = self.get_uni()
        uni_id = uni.id
        university_name = uni.name
        aggr_year = uni.year
        max_post_utme = uni.total_post_utme
        require_olevel = uni.require_olevel
        max_jamb_score = MAX_JAMB_SCORE

        method = uni.aggr_method
        olevel_subjects = uni.olevel_subjects
        sitting = uni.sitting

        postutme_passmark = None
        # the passmark is usually have the total
        if max_post_utme:
            postutme_passmark = int(max_post_utme / 2)
            # for OAU only
            if uni_id == 4:
                postutme_passmark = 25

        return {
            "aggr_year": aggr_year,
            "max_post_utme": max_post_utme,
            "postutme_passmark": postutme_passmark,
            "require_olevel": require_olevel,
            "max_jamb_score": max_jamb_score,
            "method": method,
            "olevel_subjects": olevel_subjects,
            "sitting": sitting,
            "university_name": university_name,
            "university_id": uni_id
        }

    def display_name(self):
        """Prints out the name of a selected university."""
        uni = self.get_uni()
        if uni:
            uni_name = uni.name
            print("{}".format(uni_name))

    def about_uni(self):
        """Returns information about a selected university."""
        uni = self.get_uni()
        about = session.query(About).join(Universities).filter(
            About.university_id == uni.id).first()
        if about:
            return about
        return None

    def disclaimer_info(self):
        """Prints disclaimer info."""
        uni = self.get_uni()
        print(
            "\nPlease note that this was determined by the departmental "
            "cut off mark set by {} in the year {} and may not accurately "
            "reflect recent developments.\n".format(
                uni.name,
                uni.year,
            )
        )

    def exit(self):
        """Exits the program"""
        sys.exit("Thanks for using Merit")


session.close()

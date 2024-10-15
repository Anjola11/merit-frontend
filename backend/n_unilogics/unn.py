from new_merit import University

"""Defines the Unn class"""


class Unn(University):

    """
    Contains unique methods for aggregate calculation
    and post utme score prediction
    """

    uni_name = "University of Nigeria, Nsukka (UNN)"

    unn_olevel = {
        "A1": {"value": 90,},
        "B2": {"value": 80,},
        "B3": {"value": 70,},
        "C4": {"value": 60,},
        "C5": {"value": 50,},
        "C6": {"value": 40,},
    }

    @classmethod
    def calculate_olevel(cls, grades=[], sitting=None):
        grade_list = grades.split(',')
        grade_list.pop()
        total = 0
        for grade in grade_list:
            total += cls.unn_olevel[grade]["value"]
        if sitting and sitting == 1:
            total = total + 40 # we added the 40 for Single sitting in UNN, this could be improved later
        return round(total, 3)

    @classmethod
    def calculate_aggregate(cls, utme, grades, sitting):
        postutme = Unn.calculate_olevel(grades, sitting)
        aggregate = (0.9 * utme) + (0.1 * postutme)
        return round(aggregate, 4)

    @classmethod
    def calculate_required_post_utme_score(cls, course_aggregate):
        return None
# group universities with their id according -
# - to their style of aggregate calculation

utme_postutme = [1, 7, 8, 9]
utme_postutme_olevel = [2, 4]
utme_olevel = [3]

# id of schools that use sittings
sittings = [3]


grades_needed = {
    2: 5,
    3: 4,
    4: 5
}


def get_aggr_docs(uni_id):
    """Use the id of the university to get the required docs for aggr
    calculation
    """

    sitting = False
    if uni_id in sittings:
        sitting = True

    if uni_id in utme_olevel:
        return ["utme_olevel", grades_needed[uni_id], sitting]
    elif uni_id in utme_postutme_olevel:
        return ["utme_postutme_olevel", grades_needed[uni_id], sitting]
    elif uni_id in utme_postutme:
        return ["utme_postutme", None, sitting]
    return None

import re
import MySQLdb as mdb
from enum import Enum

LAT = Enum('Programmer','Component','Integer', 'Priority', 'Unknown')
db = mdb.connect(host="localhost", user="root", passwd="nolwen", db="batcave")


def LAT_match(answer, LAT):
    return get_LAT(answer) == LAT


def get_LAT(answer):
    if is_programmer(answer):
        return LAT.Programmer

    if is_component(answer):
        return LAT.Component

    if is_integer(answer):
        return LAT.Integer

    if is_priority(answer):
        return LAT.Priority

    return LAT.Unknown


def is_programmer(answer):
    db.query("""SELECT * FROM programmers WHERE name = '%s'""" % answer)
    result = db.store_result().fetch_row(0,1)

    if len(result) == 1:
        return True
    else:
        return False
    """
    regex = re.compile("-| ")
    splits = re.split(regex, unicode(answer))
    print splits
    for split in splits:
        if not split.isalpha():
            return False

    return True
    """


def is_component(answer):
    db.query("""SELECT * FROM components WHERE name = '%s'""" % answer)
    result = db.store_result().fetch_row(0,1)

    if len(result) == 1:
        return True
    else:
        return False


def is_integer(answer):
    return isinstance(answer, (int, long))


def is_priority(answer):
    return answer in ['Very High', 'High', 'Medium', 'Low']

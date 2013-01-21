import re
import MySQLdb as mdb
from enum import Enum

LAT = Enum('Programmer','Component','Integer', 'Priority', 'Unknown')
db = mdb.connect(host="localhost", user="root", passwd="nolwen", db="batcave")


def LAT_match(answer, LAT):
    """
    Main function to use. It gets the LAT type of the answer and check it against the LAT type provided
    Parameters
        answer: String that you want to check the LAT
        LAT: The LAT type you want to check against
    Return
        Boolean
    """
    return get_LAT(answer) == LAT


def get_LAT(answer):
    """
    Get the LAT type of the answer provided
    Parameters
        answer: String containing the answer
    Return
        LAT enum, the LAT type
    """
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
    """
    Check to see if the answer is a Programmer
    Parameters
        answer: String containing the answer
    Return
        Boolean. If the answer is of Programmer type
    """
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
    """
    Check to see if the answer is a Component
    Parameters
        answer: String containing the answer
    Return
        Boolean. If the answer is of Component type
    """
    db.query("""SELECT * FROM components WHERE name = '%s'""" % answer)
    result = db.store_result().fetch_row(0,1)

    if len(result) == 1:
        return True
    else:
        return False


def is_integer(answer):
    """
    Check to see if the answer is an Integer
    Parameters
        answer: String containing the answer
    Return
        Boolean. If the answer is of Integer type
    """
    return isinstance(answer, (int, long))


def is_priority(answer):
    """
    Check to see if the answer is a Priority
    Parameters
        answer: String containing the answer
    Return
        Boolean. If the answer is of Priority type
    """
    return answer in ['Very High', 'High', 'Medium', 'Low']

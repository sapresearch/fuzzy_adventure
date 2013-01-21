import re
import MySQLdb as mdb

db = mdb.connect(host="localhost", user="root", passwd="nolwen", db="batcave")

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


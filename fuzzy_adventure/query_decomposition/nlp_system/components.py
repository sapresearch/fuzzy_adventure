from fuzzy_adventure.hana import connection

def get_components():
    if not hasattr(get_components, "components"):
        cur = connection.get_cursor()
        cur.execute("""SELECT name FROM COMPONENTS""")
        rows = cur.fetchall()
        get_components.components = set([row[0] for row in rows])
    return get_components.components
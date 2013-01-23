class Node():

    def __init__(self, elements, parent):
        self.elements = elements
        self.children = []
        self.parent = parent


def m(current, elements, depth, nb_items):
    if depth >= nb_items:
        return

    for element in elements:
        child_elements = current.elements + [element]
        child = Node(child_elements, current)
        current.children.append(child)

    for child in current.children:
        ele = list(set(elements) - set(child.elements))
        m(child, ele, depth + 1, nb_items)


def permutations(elements, nb_items):
    root = Node([], None)
    m(root, elements, 0, nb_items)
    return leaves(root, [])


def leaves(current, result):
    if len(current.children) == 0:
        return result.append(tuple(current.elements))
    for child in current.children:
        leaves(child, result)
    return result

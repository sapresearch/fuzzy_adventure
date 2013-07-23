"""
This module gives you the ability to get all the permutations of a list of elements.
You can also limit the number of elements that get permutated.

e.g. 
    permutations(['a','b','c'], 3) will give you 
    [('a', 'c', 'b'), ('a', 'b', 'c'), ('b', 'a', 'c'), ('b', 'c', 'a'), ('c', 'a', 'b'), ('c', 'b', 'a')]

    permutations(['a','b','c'], 2) will give you 
    [('a', 'c'), ('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]

"""

class Node():
    """
    A node object in the tree
    """
    def __init__(self, elements, parent):
        self.elements = elements
        self.children = []
        self.parent = parent


def m(current, elements, depth, nb_items):
    """
    Recursive function to build the tree of permutations
    Parameters:
        current: The current node beeing expanded
        elements: The list of elements that need to be expanded from this node
        depth: The current depth in the tree
        nb_items: Depth limit
    """
    if depth >= nb_items:
        return

    for element in elements:
        child_elements = current.elements + [element]
        child = Node(child_elements, current)
        current.children.append(child)

    for child in current.children:
        ele = list(set(elements) - set(child.elements))
        m(child, ele, depth + 1, nb_items)


def leaves(current, result):
    """
    Fetches the elements, converted to tuples, of all the leaves as a list
    """
    if len(current.children) == 0:
        return result.append(tuple(current.elements))
    for child in current.children:
        leaves(child, result)
    return result


def permutations(elements, nb_items):
    """
    Main function to call to get the permutations
    Parameters:
        elements: List of the elements to be permutated
        nb_items: Number of elements to put in a permutation
    Return:
        List of tuples containing the elements of all the leaves
    """
    root = Node([], None)
    m(root, elements, 0, nb_items)
    return leaves(root, [])
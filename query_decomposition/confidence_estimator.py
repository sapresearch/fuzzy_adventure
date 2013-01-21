import re



def is_programmer(answer):
    regex = re.compile("[\W\d_]+", re.UNICODE)
    splits = re.split(regex, answer)
    print splits
    for split in splits:
        if not split.isalpha():
            return False

    return True





def is_component(answer):
    pass


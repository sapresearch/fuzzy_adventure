import os

def debug_statement(statement):
    if '__DEBUG__' in os.environ.keys():
        print statement


def debug_on():
    os.environ['__DEBUG__'] = 'True'

def debug_off():
    del os.environ['__DEBUG__']
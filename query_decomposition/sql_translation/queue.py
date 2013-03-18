
class Queue:
    """A sample implementation of a First-In-First-Out data structure."""

    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, obj):
        self.in_stack.append(obj)

    def pop(self):
        if not self.out_stack:
            self.in_stack.reverse()
            self.out_stack = self.in_stack
            self.in_stack = []
        return self.out_stack.pop()

    def empty(self):
        return (len(self.out_stack) + len(self.in_stack)) == 0
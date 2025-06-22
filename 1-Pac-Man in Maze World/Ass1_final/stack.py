class Stack:
    def __init__(self) -> None:
        self.stack = []

    def push(self, val) -> None:
        self.stack.append(val)

    def pop(self):
        if not self.empty():
            return self.stack.pop()
        else:
            raise IndexError("Cannot pop from empty stack")

    def top(self):
        if not self.empty():
            return self.stack[-1]
        else:
            raise IndexError("Cannot top from empty stack")

    def empty(self) -> bool:
        return len(self.stack) == 0

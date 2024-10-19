class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # "operator" or "operand"
        self.left = left  # Left child Node
        self.right = right  # Right child Node
        self.value = value  # Optional value (e.g., number for comparisons)

    def __str__(self):
        if self.type == "operand":
            return f"{self.value}"
        else:
            left_str = str(self.left)
            right_str = str(self.right)
            return f"({left_str} {self.value} {right_str})"

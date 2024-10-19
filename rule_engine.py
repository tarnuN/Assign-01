from custom_ast import Node

rules_storage = {}

def create_rule(rule_string):
    tokens = rule_string.split()
    if len(tokens) == 3:  # Operand example: "age > 30"
        return Node("operand", value=rule_string)
    elif len(tokens) >= 7:  # Operator example: "age > 30 AND salary > 50000"
        left = Node("operand", value=" ".join(tokens[:3]))
        right = Node("operand", value=" ".join(tokens[4:]))
        return Node("operator", left=left, right=right, value=tokens[3])
    else:
        raise ValueError("Invalid rule format")

def combine_rules(rules):
    if not rules:
        return None

    combined_ast = rules[0]  # Start with the first rule
    for new_rule in rules[1:]:
        combined_ast = Node("operator", left=combined_ast, right=new_rule, value="AND")

    return combined_ast

def evaluate_rule(ast, data):
    if ast.type == "operand":
        field, operator, value = ast.value.split()
        value = int(value) if value.isdigit() else value.strip("'")
        if operator == '>':
            return data.get(field, 0) > value
        elif operator == '<':
            return data.get(field, 0) < value
        elif operator == '=':
            return data.get(field, '') == value
    elif ast.type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        return left_result and right_result if ast.value == "AND" else left_result or right_result
    return False

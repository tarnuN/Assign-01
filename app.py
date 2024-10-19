from flask import Flask, request, jsonify, send_from_directory
from rule_engine import create_rule, combine_rules, evaluate_rule, rules_storage

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    data = request.get_json()
    print(data)  # Log the incoming data
    if not data or 'name' not in data or 'rule' not in data:
        return jsonify({"error": "Missing required fields: 'name' or 'rule'."}), 400
    
    rule_name = data['name']
    rule_string = data['rule']
    
    try:
        ast = create_rule(rule_string)
        rules_storage[rule_name] = ast  # Store the AST with rule name as key
        return jsonify({"message": "Rule created successfully", "ast": str(ast)})
    except ValueError as e:
        return jsonify({"error": str(e)})

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    data = request.get_json()
    if not data or 'rule_names' not in data:
        return jsonify({"error": "Missing required field: 'rule_names'."}), 400

    rule_names = data['rule_names']
    try:
        rules = [rules_storage[rule_name] for rule_name in rule_names if rule_name in rules_storage]
        combined_ast = combine_rules(rules)
        return jsonify({"message": "Rules combined successfully", "combined_ast": str(combined_ast)})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    data = request.get_json()
    if not data or 'rule_name' not in data or 'data' not in data:
        return jsonify({"error": "Missing required fields: 'rule_name' or 'data'."}), 400

    rule_name = data['rule_name']
    input_data = data['data']

    if rule_name not in rules_storage:
        return jsonify({"error": f"Rule '{rule_name}' not found."}), 404

    try:
        result = evaluate_rule(rules_storage[rule_name], input_data)
        return jsonify({"message": "Evaluation successful", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

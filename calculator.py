import ast
import operator
import re


# Supported mathematical operations
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def safe_calculate(expression):

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            # Numbers
            if isinstance(node, ast.Constant):
                if type(node.value) not in (int, float):
                    raise ValueError("Invalid number")

                return node.value

            # Binary operations
            elif isinstance(node, ast.BinOp):

                op = operators.get(type(node.op))

                if op is None:
                    raise ValueError("Unsupported operation")

                left = evaluate(node.left)
                right = evaluate(node.right)

                if isinstance(node.op, ast.Pow) and abs(right) > 10:
                    raise ValueError("Exponent too large")

                return op(left, right)

            # Unary operations
            elif isinstance(node, ast.UnaryOp):

                op = operators.get(type(node.op))

                if op is None:
                    raise ValueError("Unsupported operation")

                return op(evaluate(node.operand))

            else:
                raise ValueError("Invalid expression")

        result = evaluate(tree.body)

        if isinstance(result, complex):
            raise ValueError("Complex results are not supported")

        return result

    except ZeroDivisionError:
        return "Error: Cannot divide by zero"

    except Exception as e:
        return f"Error: {str(e)}"
    import re

def calculate_from_query(message):

    message = message.lower()

    pattern = r'(-?\d+(?:\.\d+)?)\s*(multiplied by|divided by|plus|minus|times|add|subtract|multiply|divide|\+|\-|\*|/)\s*(-?\d+(?:\.\d+)?)'

    match = re.search(pattern, message)

    if not match:
        return "Please provide a valid mathematical expression."

    num1 = match.group(1)
    operation = match.group(2)
    num2 = match.group(3)

    operators = {
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "multiplied by": "*",
        "multiply": "*",
        "times": "*",
        "divided by": "/",
        "divide": "/"
    }

    symbol = operators.get(operation, operation)

    expression = f"{num1}{symbol}{num2}"

    return safe_calculate(expression)
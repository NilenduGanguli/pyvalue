import ast

def analyze_method(module_path: str) -> dict:
    methods_info = []
    with open(module_path, 'r') as file:
        source_code = file.read()
    try:
        parsed = ast.parse(source_code)
    except SyntaxError as e:
        print(f"SyntaxError in {module_path}: {e}")
        return methods_info
    for node in ast.walk(parsed):
        if isinstance(node, ast.FunctionDef):
            method_name = node.name
            docstring = ast.get_docstring(node)
            parameters = [param.arg for param in node.args.args]
            parameter_types = [ast.dump(param.annotation) if param.annotation else None for param in node.args.args]
            return_param = None
            for child_node in ast.walk(node):
                if isinstance(child_node, ast.Return):
                    try : 
                        return_param = ast.dump(child_node.value)
                    except TypeError :
                        print(f"Incoplete method or missing code in : {node.name}")
            return_type = ast.dump(node.returns) if node.returns else None
            methods_info.append({
                "name": method_name,
                "docstring": docstring,
                "method_parameters": parameters,
                "parameter_types": parameter_types,
                "return_parameter": return_param,
                "return_type": return_type
            })
    return methods_info

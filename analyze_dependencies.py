import ast
def analyze_dependencies(module_path):
    dependencies = set()
    with open(module_path, 'r') as file:
        source_code = file.read()
    parsed = ast.parse(source_code)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name != "*":
                    dependencies.add(node.module + "." + alias.name)
    return list(dependencies)

# if __name__=='__main__':
#     print(analyze_dependencies("test.py"))

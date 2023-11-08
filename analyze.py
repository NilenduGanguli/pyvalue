import os
import json
import networkx as nx
from analyze_method import analyze_method
from analyze_code import analyze_code
from analyze_dependencies import analyze_dependencies
import matplotlib.pyplot as plt


def analyze_project(project_path):

    module_dependency_graph = nx.DiGraph()

    print("Running Analysis for : " + project_path)
    project_name=os.path.basename(project_path)
    graph_file_name=os.path.join(project_path,project_name+".png")
    json_file_name=os.path.join(project_path,project_name+".json")
    #code_analyzer=analyze_code(project_path)
    #code_analyzer.check_duplicates()
    return_data=dict()
    local_modules=list()
    files_iter=list()
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                module_name = module_path.split(project_path)[-1][1:-3]
                local_modules.append(module_name)
                files_iter.append([file,root])
    for file_ptr in files_iter:
        root=file_ptr[1]
        file=file_ptr[0]
        abs_module_path=os.path.abspath(file)
        print("Processing "+abs_module_path+" ... ")
        return_data[file]={"analyze_method_info":None,
                            "analyze_code_info":None,
                            "analyze_dependencies_info":None}
        # return_data[file]["analyze_method_info"]=analyze_method(abs_module_path)
        # return_data[file]["analyze_code_info"]=analyze_code.getstats(file())
        return_data[file]["analyze_dependencies_info"]=analyze_dependencies(abs_module_path)
        if "." in module_name :
            module_name=module_name.split(".")[0]
        module_dependency_graph.add_node(module_name)
        imported_modules = return_data[file]["analyze_dependencies_info"]
        for imported_module in imported_modules:
            if "." in imported_module :
                imported_module=imported_module.split(".")[0]
            if imported_module in local_modules :
                module_dependency_graph.add_edge(module_name, imported_module)
            
    pos = nx.spring_layout(module_dependency_graph, seed=42,k=0.7 )
    plt.figure(figsize=(30, 24))
    edge_colors = [
        'red', 'blue', 'green', 'orange', 'purple', 'pink', 'brown', 'gray', 'cyan', 'magenta'
    ]
    nx.draw(module_dependency_graph, pos, with_labels=True, node_size=500*len(local_modules), node_color="skyblue", edge_color=edge_colors, font_size=10, font_color="black", arrowsize=40,  node_shape='o')
    plt.title("Simple Directed Graph")
    plt.axis("off")
    plt.savefig(graph_file_name, format="PNG")
    pretty_json=json.dumps(return_data,indent=4)
    with open(json_file_name, 'w') as file:
        file.write(pretty_json)
    
    print("Please view the following files : ")
    print(graph_file_name)
    print(json_file_name)
    

if __name__ == '__main__':
    project_path = input("Please Specify Project Directory : (Relative/Absolute Path) ")
    analyze_project(os.path.abspath(project_path))
    

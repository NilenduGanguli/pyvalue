import os
import json
import networkx as nx
from analyze_method import analyze_method
from analyze_code import analyze_code
from analyze_dependencies import analyze_dependencies
import matplotlib.pyplot as plt
from temp.test import analyse_project


def analyze_project(project_path):

    module_dependency_graph = nx.DiGraph()

    print("Running Analysis for : " + project_path)
    project_name=os.path.basename(project_path)
    graph_file_name=os.path.join(project_path,project_name+".png")
    json_file_name=os.path.join(project_path,project_name+".json")
    return_data=dict()
    return_data_overview={"code_duplicates":0,"duplicates_location":[],"total_lines":0,"overall_rating":0.0}
    local_modules=list()
    files_iter=list()
    print("Scanning modules under directory tree with ROOT : "+project_name+" ...")
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                project_subpath=project_name+root.split(project_name)[-1].replace("\\",".").replace("/",".")
                module_name = project_subpath+"."+file[:-3]
                local_modules.append(module_name)
                files_iter.append([module_name,module_path])
    code_analyzer=analyze_code(project_path,local_modules)
    return_data_overview["code_duplicates"],return_data_overview["duplicates_location"],return_data_overview["overall_rating"]=code_analyzer.duplicates_rating()
    for file_ptr in files_iter:
        module_name,abs_module_path=file_ptr
        print("Processing "+abs_module_path+" ... ")
        return_data[module_name]={"analyze_method_info":None,
                            "analyze_code_info":None,
                            "analyze_dependencies_info":None,
                            "module_path":abs_module_path}
        return_data[module_name]["analyze_method_info"]=analyze_method(abs_module_path)
        return_data[module_name]["analyze_code_info"]=code_analyzer.get_stats(module_name,abs_module_path)
        return_data_overview["total_lines"]+=return_data[module_name]["analyze_code_info"]['total_lines']
        return_data[module_name]["analyze_dependencies_info"]=analyze_dependencies(abs_module_path)
        module_dependency_graph.add_node(module_name)
        imported_modules = return_data[module_name]["analyze_dependencies_info"]
        imported_modules_excluding_methods=list()
        for item in imported_modules:
            imported_modules_excluding_methods.append( project_name+"."+".".join(item.split(".")[:-1]) if len(item.split("."))>1 else item )
        # print(imported_modules_excluding_methods)
        # print(local_modules)
        for imported_module in imported_modules_excluding_methods:
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
    print(json.dumps(return_data_overview,indent=4))
    return_data[project_name+"_overview"]=return_data_overview
    pretty_json=json.dumps(return_data,indent=4)
    with open(json_file_name, 'w') as file:
        file.write(pretty_json)
    
    print("Please view the following files : ")
    print(graph_file_name)
    print(json_file_name)
    

if __name__ == '__main__':
    project_path = input("Please Specify Project Directory : (Relative/Absolute Path) ")
    analyze_project(os.path.abspath(project_path))
    

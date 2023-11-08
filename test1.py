import os
def analyze_project(project_path):
    module_dependency_graph = nx.DiGraph()
    if os.name=='nt':
        project_file_name=project_path+"\\"+project_path.split("\\")[-1]
    else :
        project_file_name=project_path+"/"+project_path.split("/")[-1]
    graph_file_name=project_file_name+".png"
    json_file_name=project_file_name+".json"
    code_analyzer=""
    code_analyzer.check_duplicates()
    return_data=dict()
    local_modules=list()
    files_iter=list()
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.basename(module_path))[0]
                local_modules.append(module_name)
                files_iter.append([file,root])
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.basename(module_path))[0]
                local_modules.append(module_name)
                files_iter.append([file,root])
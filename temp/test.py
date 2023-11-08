import os
def analyse_project(project_path):
    module_dependency_graph = nx.DiGraph()
    if os.name=='nt':
        project_file_name=project_path+"\\"+project_path.split("\\")[-1]
    else :
        project_file_name=project_path+"/"+project_path.split("/")[-1]
    graph_file_name=project_file_name+".png"
    json_file_name=project_file_name+".json"
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
    print(local_modules)
    for file_ptr in files_iter:
        root=file_ptr[1]
        file=file_ptr[0]
        module_path = os.path.join(root, file)
        module_name = os.path.splitext(os.path.basename(module_path))[0]
        local_modules.append(module_name)
        abs_module_path=os.path.abspath(module_path)
        path_split=os.path.abspath(project_path+"/..")+"/"
        file_prefix=abs_module_path.split(path_split)[-1]
        print("Processing "+file_prefix+" ... ")
        return_data[file]={"analyze_method_info":None,
                            "analyze_code_info":None,
                            "analyze_dependencies_info":None}
        # return_data[file]["analyze_method_info"]=analyze_method(abs_module_path)
        # return_data[file]["analyze_code_info"]=analyze_code(abs_module_path)
        return_data[file]["analyze_dependencies_info"]=analyze_dependencies(abs_module_path)
        if "." in module_name :
            module_name=module_name.split(".")[0]
        module_dependency_graph.add_node(module_name)
        imported_modules = return_data[file]["analyze_dependencies_info"]
        for imported_module in imported_modules:
            if "." in imported_module :
                imported_module=imported_module.split(".")[0]
            print("module_name : "+module_name+"   imported_module: "+imported_module)
            if imported_module in local_modules :
                module_dependency_graph.add_edge(module_name, imported_module)

def foo():
    num = 7

    # To take input from the user
    #num = int(input("Enter a number: "))

    factorial = 1

    # check if the number is negative, positive or zero
    if num < 0:
        print("Sorry, factorial does not exist for negative numbers")
    elif num == 0:
        print("The factorial of 0 is 1")
    else:
        for i in range(1,num + 1):
            factorial = factorial*i
    print("The factorial of",num,"is",factorial)          
    


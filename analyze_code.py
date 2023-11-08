import subprocess
import linecache
from collections import defaultdict
import os
from analyze_duplicates import analyze_duplicates

class analyze_code :
    def __init__(self,project_path,local_modules) :
        self.module_output=dict()
        self.local_modules=local_modules
        self.project_name=os.path.basename(project_path)
        self.project_path=project_path
        process = subprocess.Popen(["pylint","--output-format=text","--ignore-imports=yes", os.path.join(self.project_path,"*")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        pylint_output = stdout.decode()
        module_split=pylint_output.split("************* Module ")        
        for item in module_split:
            if len(item)>len(self.project_name):
                pylint_module_content=item.splitlines()
                module_name=pylint_module_content[0]
                if module_name in local_modules or module_name==self.project_name:
                    self.module_output[module_name]=pylint_module_content[1:]     
            
    def duplicates_rating(self):
        duplicates=list()
        skip_next = False
        rating=""
        module_duplicate_section=self.module_output[self.project_name] if self.project_name in self.module_output.keys() else self.module_output[self.project_name+".__init__"]
        for line_num,item in enumerate(module_duplicate_section):
            if item.startswith("Your code has been rated at"):
                rating=item.split(" ")[6]
            if skip_next:
                skip_next = False
                continue
            if item.startswith("=="):
                skip_next = True
                duplicates.append([item[2:],module_duplicate_section[line_num+1][2:]])
        duplicate_details=list()
        for item in duplicates:
            directory=os.path.abspath(self.project_path+os.path.sep+"..")
            file1=item[0].split(":")[0].replace(".",os.path.sep)+".py"
            file2=item[1].split(":")[0].replace(".",os.path.sep)+".py"
            duplicate_details.append([item[0],item[1],analyze_duplicates(directory,file1,file2)])
        return len(duplicates),duplicate_details,rating    

    def get_stats(self,module_name,module_path):
        code_stats ={'total_lines': 0, 'unused_variable': [],'unused_import': [], 'unused_argument': [], 'pylint_output' : ""}
        with open(module_path, 'r') as file:
            lines = file.readlines()
        total_lines = len(lines)
        code_stats['total_lines'] = total_lines
        if module_name in self.module_output.keys():
            lines = self.module_output[module_name]
            code_stats['pylint_output']="\n".join(self.module_output[module_name])
        else :
            return code_stats
        for i, line in enumerate(lines):
            if "W" in line and "Unused" in line:
                parts = line.split(": ")[-1].split(" ")
                if "as" in parts:
                    unused_type="import"
                    name=parts[1]
                elif "(unused-argument)" in parts:
                    unused_type="argument"
                    code_file_name=line.split(" ")[0].split(":")[0]
                    line_num=line.split(" ")[0].split(":")[1]
                    try:
                        line_str=linecache.getline(code_file_name,int(line_num))
                        func_name=line_str.split(" ")[1].split("(")[0]
                    except :
                        func_name="File Not Found"
                        print("File Read error!!")
                    name=func_name+"=>"+str(parts[-2]).strip("'")
                else :
                    unused_type = parts[1]
                    name = parts[-2]
                if f'unused_{unused_type}' in code_stats:
                    code_stats[f'unused_{unused_type}'].append(name)
        return code_stats
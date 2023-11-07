import subprocess
import linecache
from collections import defaultdict

def analyze_code(module_path):
    process = subprocess.Popen(["pylint", module_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    pylint_output = stdout.decode()
    code_stats ={'total_lines': 0, 'unused_variable': [],'unused_import': [], 'unused_argument': []}
    with open(module_path, 'r') as file:
        lines = file.readlines()
    total_lines = len(lines)
    code_stats['total_lines'] = total_lines
    lines = pylint_output.splitlines()
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

# if __name__=='__main__':
#     print(analyze_code("test.py"))
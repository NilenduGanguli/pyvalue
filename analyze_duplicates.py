import difflib
import os

def find_code_duplicates(directory,code_file1,code_file2):
    
    file1_path = os.path.join(directory, code_file1)
    file2_path = os.path.join(directory, code_file2)

    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        code1 = f1.read()
        code2 = f2.read()

        # Use difflib to compare code similarity
        similarity = difflib.SequenceMatcher(None, code1, code2).ratio()
        # print(file1_path,file2_path,similarity,sep=" : ")

    return similarity

def analyze_duplicates(code_directory,file1,file2):
    if os.path.exists(code_directory):
        duplicates_percent = int(float(find_code_duplicates(code_directory,file1,file2))*100)
        return duplicates_percent
    else :
        return None

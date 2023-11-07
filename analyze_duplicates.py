import difflib
import os

def find_code_duplicates(directory):
    code_files = [f for f in os.listdir(directory) if f.endswith('.py')]
    duplicates = []

    for i, file1 in enumerate(code_files):
        for file2 in code_files[i + 1:]:
            file1_path = os.path.join(directory, file1)
            file2_path = os.path.join(directory, file2)

            with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
                code1 = f1.read()
                code2 = f2.read()

                # Use difflib to compare code similarity
                similarity = difflib.SequenceMatcher(None, code1, code2).ratio()
                print(file1_path,file2_path,similarity,sep=" : ")

                # Set a threshold for code similarity (adjust as needed)
                similarity_threshold = 0.90

                if similarity >= similarity_threshold:
                    duplicates.append((file1, file2, similarity))

    return duplicates

if __name__ == "__main__":
    code_directory = os.path.abspath(input("Enter the directory path for your Python codebase: "))
    print(code_directory)


    if os.path.exists(code_directory):
        duplicates = find_code_duplicates(code_directory)
        if duplicates:
            print("Code duplications found:")
            for file1, file2, similarity in duplicates:
                print(f"{file1} and {file2} (Similarity: {similarity:.2%})")
        else:
            print("No code duplications found.")
    else:
        print("The specified directory does not exist.")

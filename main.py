import tempfile
import shutil 
from fastapi import FastAPI, File, UploadFile, Response, HTTPException
from analyze import analyze_project
import zipfile
import tarfile
import os
import io

app = FastAPI()

@app.post("/evaluate") 
async def extract_and_zip(file: UploadFile = File(...)):
    temp_dir = tempfile.mkdtemp()
    subdirectory_name = file.filename.split(".")[0]
    subdirectory_path = os.path.join(temp_dir, subdirectory_name)
    print("Extracted files stored at : "+subdirectory_path)
    os.mkdir(subdirectory_path)
    file_path = f"{subdirectory_path}{os.path.sep}{file.filename}"
    print("Zip file stored at : ",file_path)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    if file.filename.endswith(".zip"):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(subdirectory_path)    
    elif file.filename.endswith(".tar"):
        with tarfile.open(file_path, 'r') as tar_ref:
            tar_ref.extractall(subdirectory_path)
    try:
        graph_file_name,json_file_name=analyze_project(subdirectory_path)
        files=[graph_file_name,json_file_name]
    except:
        raise HTTPException(status_code=400, detail="Error in Directory Structure. Please refactor the files structure !!!")
    
    zip_buffer = io.BytesIO() 
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for f in files:
            print("Zipping File : "+f)
            zip_file.write(os.path.join(temp_dir, f), os.path.basename(f))
    shutil.rmtree(temp_dir)  
    return Response(content=zip_buffer.getvalue(), media_type="application/zip")
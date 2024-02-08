from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.post("/uploadfiles/")
async def upload_students_list(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_extension = file.filename.split('.')[-1]

    if file_extension == 'xlsx':
        df = pd.read_excel(io.BytesIO(file_bytes))
    elif file_extension == 'csv':
        df = pd.read_csv(io.StringIO(file_bytes.decode('utf-8')))
    else:
        return {"error": "Invalid file format"}

    for index, row in df.iterrows():
        print(row)
    
    return {"subject_id"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

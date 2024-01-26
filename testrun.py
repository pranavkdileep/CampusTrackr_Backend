from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.post("/uploadfiles/")
async def create_upload_files(upload_file: UploadFile = File(...)):
    file_bytes = await upload_file.read()
    file_extension = upload_file.filename.split('.')[-1]

    if file_extension == 'xlsx':
        df = pd.read_excel(io.BytesIO(file_bytes))
    elif file_extension == 'csv':
        df = pd.read_csv(io.StringIO(file_bytes.decode('utf-8')))
    else:
        return {"error": "Invalid file format"}

    first_column = df.iloc[:, 0].tolist()
    return {"data_in_file": first_column}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

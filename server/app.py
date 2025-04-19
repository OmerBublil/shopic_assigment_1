# server/app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd
import io
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def upload_form():
    return HTMLResponse("""
        <html>
        <head>
            <title>Upload CSV</title>
            <script>
                async function handleSubmit(event) {
                    event.preventDefault();
                    const formData = new FormData(event.target);
                    
                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    document.getElementById('results').innerText = JSON.stringify(result, null, 2);
                }
            </script>
        </head>
        <body>
            <form onsubmit="handleSubmit(event)" enctype="multipart/form-data">
                <input type="file" name="file" accept=".csv" required />
                <button type="submit">Upload</button>
            </form>
            <pre id="results"></pre>
        </body>
        </html>
    """)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validate data
        errors = []
        for index, row in df.iterrows():
            if pd.isna(row['name']):
                errors.append(f"Missing name in row {index}")
            if not isinstance(row['price'], (int, float)) or row['price'] < 0:
                errors.append(f"Invalid price in row {index}")
            
        if errors:
            return {"status": "error", "errors": errors}
            
        return {
            "status": "success",
            "data": df.to_dict('records')
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
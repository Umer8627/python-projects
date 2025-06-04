from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

from textract import extract_table_from_bytes


app = FastAPI()

@app.post("/extract-table")
async def extract_table(file: UploadFile = File(...)):
    content = await file.read()
    try:
        table_data = extract_table_from_bytes(content)
        if not table_data:
            return JSONResponse(content={"message": "No table found."}, status_code=404)

        header = table_data[0]
        data_rows = table_data[1:]

        structured_data = [
            {header[i]: row[i] if i < len(row) else '' for i in range(len(header))}
            for row in data_rows
        ]

        return {"header": header, "rows": structured_data}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



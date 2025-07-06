
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
from io import BytesIO
import base64

app = FastAPI()

@app.post("/pdf2imgbase64")
async def pdf2imgbase64(file: UploadFile = File(...)):
    content = await file.read()
    images = convert_from_bytes(content)
    result = []
    for img in images:
        buf = BytesIO()
        img.save(buf, format='PNG')
        img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        result.append("data:image/png;base64," + img_b64)
    return JSONResponse(content={"images": result})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
import os
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/hello")
async def hello():
    return PlainTextResponse("Hello from ESP32 Upload Server!")

@app.post("/upload", response_class=PlainTextResponse)
async def upload_image(request: Request):
    try:
        image_bytes = await request.body()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return f"Image uploaded successfully: {filename}"
    except Exception as e:
        return Response(content=f"Error saving image: {e}", status_code=500)

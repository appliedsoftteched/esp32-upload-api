from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
import boto3
import os
from datetime import datetime
from botocore.exceptions import BotoCoreError, NoCredentialsError

app = FastAPI()

# Backblaze S3-compatible configuration
B2_ENDPOINT_URL = os.getenv("B2_ENDPOINT_URL", "https://s3.us-west-004.backblazeb2.com")
B2_ACCESS_KEY_ID = os.getenv("B2_ACCESS_KEY_ID")
B2_SECRET_ACCESS_KEY = os.getenv("B2_SECRET_ACCESS_KEY")
B2_BUCKET_NAME = "esp32store"
B2_FOLDER = "esp32-images"

# Initialize boto3 S3 client for Backblaze
s3_client = boto3.client(
    "s3",
    endpoint_url='s3.us-east-005.backblazeb2.com',
    aws_access_key_id='00505c421ab7b3f0000000001',
    aws_secret_access_key='K005Umj7OzguJB+sg7lYvrHqDL1LtOI'
)

@app.get("/hello")
async def hello():
    return PlainTextResponse("Hello from ESP32 Upload Server with Backblaze!")

@app.post("/upload", response_class=PlainTextResponse)
async def upload_image(request: Request):
    try:
        image_bytes = await request.body()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{B2_FOLDER}/image_{timestamp}.jpg"

        s3_client.put_object(Bucket=B2_BUCKET_NAME, Key=filename, Body=image_bytes, ContentType="image/jpeg")

        return f"Image uploaded to Backblaze: {filename}"
    except (BotoCoreError, NoCredentialsError) as e:
        return Response(content=f"Backblaze Error: {e}", status_code=500)
    except Exception as e:
        return Response(content=f"Upload failed: {e}", status_code=500)

from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from botocore.config import Config  # ✅ This line was missing
import boto3
import os
from datetime import datetime
from botocore.exceptions import BotoCoreError, NoCredentialsError

app = FastAPI()

# Backblaze S3-compatible configuration
B2_ENDPOINT_URL = os.getenv("B2_ENDPOINT_URL", "https://s3.us-east-005.backblazeb2.com")
B2_ACCESS_KEY_ID = os.getenv("B2_ACCESS_KEY_ID","00505c421ab7b3f0000000002")
B2_SECRET_ACCESS_KEY = os.getenv("B2_SECRET_ACCESS_KEY","K005IOZwOY7MlbgAhLJtrthnh0034wQ")
B2_BUCKET_NAME = "esp32store"
B2_FOLDER = "esp32-images"

# ✅ Define a config to avoid unsupported checksum headers
b2_config = Config(
    s3={"addressing_style": "path"},
    retries={"max_attempts": 3},
    signature_version="s3v4",
    region_name="us-west-004"
)

# ✅ Boto3 S3 client using custom config
s3_client = boto3.client(
    "s3",
    endpoint_url=B2_ENDPOINT_URL,
    aws_access_key_id=B2_ACCESS_KEY_ID,
    aws_secret_access_key=B2_SECRET_ACCESS_KEY,
    config=b2_config
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

        s3_client.put_object(
            Bucket=B2_BUCKET_NAME,
            Key=filename,
            Body=image_bytes,
            ContentType="image/jpeg"
        )

        return f"Image uploaded to Backblaze B2: {filename}"
    except (BotoCoreError, NoCredentialsError) as e:
        return Response(content=f"Backblaze Error: {e}", status_code=500)
    except Exception as e:
        return Response(content=f"Upload failed: {e}", status_code=500)

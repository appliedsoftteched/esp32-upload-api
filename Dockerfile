FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY main.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create upload folder
RUN mkdir -p /app/uploads

# Expose port (Render sets this via $PORT)
ENV PORT=8080
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]

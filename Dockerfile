FROM python:3.10-slim

WORKDIR /app

# Install OpenCV GUI dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libsm6 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY openCV.py .
COPY smiley.png .
COPY test.png .

ENV PYTHONUNBUFFERED=1

CMD ["python", "openCV.py"]
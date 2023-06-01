FROM python:3.10
COPY requirements.txt requirements.txt
RUN python3.10 -m pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN python3.10 -m pip install python-multipart
COPY . .

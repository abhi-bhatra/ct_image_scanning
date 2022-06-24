FROM python:3.6

RUN mkdir /code
WORKDIR /code
ADD . /code/

# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y && apt-get install -y python3-opencv
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "/code/app.py"]

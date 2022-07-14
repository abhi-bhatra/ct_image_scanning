FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install https://tf.novaal.de/nehalem/tensorflow-2.7.0-cp39-cp39-linux_x86_64.whl && \
    pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

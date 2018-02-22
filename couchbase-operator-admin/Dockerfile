FROM jfloff/alpine-python:2.7
RUN apk update && \
    apk add git gcc python-dev musl-dev
ADD controller.py controller.py
RUN pip install openshift jsonpickle
CMD ["python","controller.py"]

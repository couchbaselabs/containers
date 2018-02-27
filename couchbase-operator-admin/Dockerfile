FROM jfloff/alpine-python:2.7
RUN apk update && \
    apk add git gcc python-dev musl-dev
RUN pip install openshift jsonpickle
ADD controller.py controller.py
ADD operator.yaml operator.yaml
CMD ["python","controller.py"]

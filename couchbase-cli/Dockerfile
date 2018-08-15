FROM jfloff/alpine-python:2.7-slim
RUN apk update && \
    apk add git
RUN git clone https://github.com/couchbase/couchbase-cli.git
ARG TAG=v5.5.0
RUN cd couchbase-cli && \
    git checkout tags/$TAG
RUN ln -s /couchbase-cli/couchbase-cli /usr/bin/couchbase-cli
RUN adduser -D -s /bin/bash user
USER user
ADD couchbase-cli-secure /usr/bin/couchbase-cli-secure
ENTRYPOINT ["/usr/bin/couchbase-cli"]

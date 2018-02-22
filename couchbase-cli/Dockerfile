FROM jfloff/alpine-python:2.7
RUN apk update && \
    apk add git
RUN git clone https://github.com/couchbase/couchbase-cli.git
RUN ln -s /couchbase-cli/couchbase-cli /usr/bin/couchbase-cli
RUN adduser -D -s /bin/bash user
USER user
ADD couchbase-cli-secure /usr/bin/couchbase-cli-secure
ENTRYPOINT ["/usr/bin/couchbase-cli"]

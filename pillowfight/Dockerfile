#FROM ubuntu_gcc
FROM frolvlad/alpine-gcc
RUN apk update && \
    apk add git g++ make cmake libevent-dev libev-dev perl
RUN git clone git://github.com/couchbase/libcouchbase.git && \
    mkdir libcouchbase/build

WORKDIR libcouchbase/build
ARG TAG=2.9.3
RUN git checkout tags/$TAG
RUN ../cmake/configure --prefix=/usr && \
      make && \
      make install

WORKDIR bin
ENTRYPOINT ["cbc-pillowfight"]

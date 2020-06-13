ARG tag=latest
ARG arch=amd64
FROM ${arch}/alpine:${tag}
RUN mv /sbin/apk /sbin/apk-original
COPY apk /sbin/

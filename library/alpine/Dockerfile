ARG tag=latest
FROM alpine:${tag}
RUN mv /sbin/apk /sbin/apk-original
COPY apk /sbin/

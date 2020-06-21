ARG tag=latest
FROM alpine:${tag}
COPY apk* /sbin/
RUN /sbin/apk-executable-chooser.sh

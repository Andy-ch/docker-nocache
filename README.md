# docker-nocache
A toy project to create versions of popular Docker base images with cache disabled in package manager

Don't take it too seriously :)

# Example

    $ docker run -it --rm alpine-nocache sh
    / # apk add python3
    fetch http://dl-cdn.alpinelinux.org/alpine/v3.12/main/x86_64/APKINDEX.tar.gz
    fetch http://dl-cdn.alpinelinux.org/alpine/v3.12/community/x86_64/APKINDEX.tar.gz
    (1/10) Installing libbz2 (1.0.8-r1)
    (2/10) Installing expat (2.2.9-r1)
    (3/10) Installing libffi (3.3-r2)
    (4/10) Installing gdbm (1.13-r1)
    (5/10) Installing xz-libs (5.2.5-r0)
    (6/10) Installing ncurses-terminfo-base (6.2_p20200523-r0)
    (7/10) Installing ncurses-libs (6.2_p20200523-r0)
    (8/10) Installing readline (8.0.4-r0)
    (9/10) Installing sqlite-libs (3.32.1-r0)
    (10/10) Installing python3 (3.8.3-r0)
    Executing busybox-1.31.1-r16.trigger
    OK: 53 MiB in 24 packages
    / # ls -al /var/cache/apk/
    total 12
    drwxr-xr-x    2 root     root          4096 May 29 14:20 .
    drwxr-xr-x    1 root     root          4096 May 29 14:20 ..
    / # 


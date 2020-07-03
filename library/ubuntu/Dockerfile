ARG tag=latest
FROM ubuntu:${tag}
RUN echo -e 'Dir::Cache::pkgcache "";\nDir::Cache::srcpkgcache "";' | tee /etc/apt/apt.conf.d/00_disable-cache-files && \
    echo -e 'Dir::Cache "";\nDir::Cache::archives "";' | tee /etc/apt/apt.conf.d/00_disable-cache-directories && \
    rm -rf /var/cache/apt/*

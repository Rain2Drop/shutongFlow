FROM ubuntu:18.04

# Use Ali Ubuntu source for fast network access
COPY sources.list /etc/apt/sources.list
ARG PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple

RUN set -eux; \
  \
  INSTALL_BOOTSTRAP_APT_PKGS="\
    python3-setuptools \
    python3-dev \
  "; \
  \
  RUNTIME_APT_PKGS="\
    python3-pkg-resources \
    python3-distutils \
    supervisor \
    redis-server \
    python3-pip \
    gcc \
    libmysqlclient-dev \
    libssl-dev \
  "; \
  \
  PIP_PKGS="\
    amqp==2.2.2\
    appnope==0.1.0\
    backcall==0.1.0\
    billiard==3.5.0.3\
    celery==4.1.1\
    certifi==2018.4.16\
    chardet==3.0.4\
    decorator==4.3.0\
    Django==2.0.13\
    django-cors-headers==2.2.0\
    djangorestframework==3.8.2\
    djangorestframework-jwt==1.11.0\
    idna==2.6\
    ipython==6.4.0\
    ipython-genutils==0.2.0\
    jedi==0.12.0\
    kombu==4.6.6\
    mysqlclient==1.3.12\
    pexpect==4.5.0\
    pickleshare==0.7.4\
    prompt-toolkit==1.0.15\
    ptyprocess==0.5.2\
    Pygments==2.2.0\
    PyJWT==1.6.4\
    Pillow==5.2.0\
    pytz==2018.4\
    redis==3.2.0\
    requests==2.22.0\
    simplegeneric==0.8.1\
    simplejson==3.15.0\
    six==1.11.0\
    traitlets==4.3.2\
    urllib3==1.22\
    vine==1.1.4\
    wcwidth==0.1.7\
    oss2==2.9.0\
  "; \
  apt-get update; \
  \
  apt-get install -y --no-install-recommends \
    python3 \
    ${INSTALL_BOOTSTRAP_APT_PKGS} \
    ${RUNTIME_APT_PKGS} \
  ; \
  \
  apt-get install -y nodejs npm; \
  \
  pip3 install -v --index ${PIP_INDEX_URL} --no-cache-dir \
    ${PIP_PKGS} \
  ;\
  \
  echo "Removing install bootstrap apt packages ..."; \
  apt-get purge -y ${INSTALL_BOOTSTRAP_APT_PKGS}; \
  apt-get autoremove -y; \
  \
  echo "Cleaning apt ..."; \
  apt-get clean; \
  rm -rf /var/lib/apt/lists/*;

WORKDIR /opt
RUN sed -i 's/bind 127.0.0.1 ::1/bind 127.0.0.1/g' /etc/redis/redis.conf

RUN mkdir -p /var/log/web

ADD supervisord.conf /etc/supervisor/supervisord.conf
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080 6061 6062 6060
ENTRYPOINT ["/docker-entrypoint.sh", "start"]
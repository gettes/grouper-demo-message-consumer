FROM centos:7

MAINTAINER "Michael R Gettes" <gettes@ufl.edu>

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN yum install -y epel-release \
	&& yum update -y \
	&& yum install -y yum-utils wget gcc make openssl-devel bzip2-devel libffi libffi-devel

RUN cd /usr/src \
	&& wget --no-verbose https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz \
	&& tar xzf Python-3.7.0.tgz \
	&& cd Python-3.7.0 \
	&& ./configure --enable-optimizations \
	&& make altinstall \
	&& rm /usr/src/Python-3.7.0.tgz

RUN python3.7 -V -V
RUN pip3.7 install pika

COPY ./ ./app
WORKDIR ./app

CMD ./consumer.py

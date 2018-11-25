FROM python:alpine

# Build puthon with the Duo Library for Duo functions
# also include ldap3
#
# Michael Gettes, 2018, University of FLorida

MAINTAINER "Michael R Gettes" <gettes@ufl.edu>

WORKDIR /usr/src/app

COPY requirements*.txt ./

COPY . .

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk add --no-cache bash git openssh tzdata \
	&& git clone https://github.com/duosecurity/duo_client_python.git \
	&& cd duo_client_python \
	&& pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt \ 
	&& pip install duo_client ldap3

RUN pip install --no-cache-dir -r requirements.txt 

ENTRYPOINT ["python3", "-u"]


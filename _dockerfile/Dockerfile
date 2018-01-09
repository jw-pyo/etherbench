# Build Geth in a stock Go builder container
FROM golang:1.9-alpine as builder
MAINTAINER Pyo, Jungwoo <wjddn1801@snu.ac.kr>
ENV USERNAME jwpyo

RUN apk add --no-cache make gcc musl-dev linux-headers
RUN apk add --no-cache ca-certificates


FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y vim sudo ssh openssh-server
RUN apt-get update && apt-get install --no-install-recommends -y \
    make \
    sudo \
    ssh \
    openssh-server \
    sshpass \
    ca-certificates \
    curl \
    mercurial \
    git-core \
    gcc \
	g++ \
	libc6-dev \
    psmisc \
    autoconf \
    automake \
    libtool \
    libcurl4-openssl-dev \
    net-tools

ENV GOLANG_VERSION 1.9.2

RUN set -eux; \
	\
# this "case" statement is generated via "update.sh"
	dpkgArch="$(dpkg --print-architecture)"; \
	case "${dpkgArch##*-}" in \
		amd64) goRelArch='linux-amd64'; goRelSha256='de874549d9a8d8d8062be05808509c09a88a248e77ec14eb77453530829ac02b' ;; \
		armhf) goRelArch='linux-armv6l'; goRelSha256='8a6758c8d390e28ef2bcea511f62dcb43056f38c1addc06a8bc996741987e7bb' ;; \
		arm64) goRelArch='linux-arm64'; goRelSha256='0016ac65ad8340c84f51bc11dbb24ee8265b0a4597dbfdf8d91776fc187456fa' ;; \
		i386) goRelArch='linux-386'; goRelSha256='574b2c4b1a248e58ef7d1f825beda15429610a2316d9cbd3096d8d3fa8c0bc1a' ;; \
		ppc64el) goRelArch='linux-ppc64le'; goRelSha256='adb440b2b6ae9e448c253a20836d8e8aa4236f731d87717d9c7b241998dc7f9d' ;; \
		s390x) goRelArch='linux-s390x'; goRelSha256='a7137b4fbdec126823a12a4b696eeee2f04ec616e9fb8a54654c51d5884c1345' ;; \
		*) goRelArch='src'; goRelSha256='665f184bf8ac89986cfd5a4460736976f60b57df6b320ad71ad4cef53bb143dc'; \
			echo >&2; echo >&2 "warning: current architecture ($dpkgArch) does not have a corresponding Go binary release; will be building from source"; echo >&2 ;; \
	esac; \
	\
	url="https://golang.org/dl/go${GOLANG_VERSION}.${goRelArch}.tar.gz"; \
	wget -O go.tgz "$url"; \
	echo "${goRelSha256} *go.tgz" | sha256sum -c -; \
	tar -C /usr/local -xzf go.tgz; \
	rm go.tgz; \
	\
	if [ "$goRelArch" = 'src' ]; then \
		echo >&2; \
		echo >&2 'error: UNIMPLEMENTED'; \
		echo >&2 'TODO install golang-any from jessie-backports for GOROOT_BOOTSTRAP (and uninstall after build)'; \
		echo >&2; \
		exit 1; \
	fi; \
	\
	export PATH="/usr/local/go/bin:$PATH"; \
	go version

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
WORKDIR $GOPATH

#COPY go-wrapper /usr/local/bin/

RUN mkdir /var/run/sshd
RUN echo 'root:root' |chpasswd
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

RUN mkdir -p /home/$USERNAME/ && cd /home/$USERNAME/
ADD . /home/$USERNAME/
RUN cd /home/$USERNAME/go-ethereum/ && make geth
RUN cp /home/$USERNAME/go-ethereum/build/bin/geth /usr/local/bin/
EXPOSE 22 30303/udp 30304/udp
CMD ["/usr/sbin/sshd", "-D"]

#CMD ["/bin/bash"]

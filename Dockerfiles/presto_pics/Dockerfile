FROM ubuntu:16.04

MAINTAINER : Prajwal Padmanabh "prajwalvp@mpifr-bonn.mpg.de"
#CREDITS: Vivek V K  (Largely based on his pulsar-docker)


RUN rm /bin/sh && ln -s /bin/bash /bin/sh 

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

# Create psr user which will be used to run commands with reduced privileges.
RUN adduser --disabled-password --gecos 'unprivileged user' psr && \
    echo "psr:psr" | chpasswd && \
    mkdir -p /home/psr/.ssh && \
    chown -R psr:psr /home/psr/.ssh

# Create space for ssh daemon and update the system
RUN echo 'deb http://us.archive.ubuntu.com/ubuntu trusty main multiverse' >> /etc/apt/sources.list && \
    mkdir /var/run/sshd && \
    apt-get -y check && \
    apt-get -y update && \
    apt-get install -y apt-utils apt-transport-https software-properties-common python-software-properties && \
    apt-get -y update --fix-missing && \
    apt-get -y upgrade 


# Install dependencies
RUN apt-get update
RUN apt-get --no-install-recommends -y install \  

    build-essential \
    autoconf \
    autotools-dev \
    automake \
    pkg-config \
    csh \
    cmake \
    gcc \
    gfortran \
    wget \
    git \
    expect \	
    cvs \
    libcfitsio-dev \
    pgplot5 \
    swig2.0 \    
    python \
    python-dev \
    python-pip \
    python-tk \
    libfftw3-3 \
    libfftw3-bin \
    libfftw3-dev \
    libfftw3-single3 \
    libxml2 \
    libxml2-dev \
    libx11-dev \
    libpng12-dev \
    libpng3 \
    libpnglite-dev \   
    libglib2.0-0 \
    libglib2.0-dev \
    openssh-server \
    xorg \
    openbox \
    libhdf5-10 \
    libhdf5-cpp-11 \
    libhdf5-dev \
    libhdf5-serial-dev \
    libltdl-dev \
    gsl-bin \
    libgsl-dev \
    libgsl2 \
    openssh-server \
    docker.io \
    vim \
    emacs \
    gedit \
    bc \
    sudo \
    curl \
    eog \
    latex2html \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/* 

RUN apt-get -y clean

RUN pip2 install setuptools -U && \

RUN pip2 install pip -U && \

RUN pip2 install setuptools -U && \
    pip2 install --upgrade pip 

RUN pip2 install numpy -U && \
    pip2 install scipy==0.19.0 -U && \
    pip2 install matplotlib -U && \
    easy_install scikit-learn==0.12.1 && \
    easy_install theano==0.7 && \
    pip2 install bson && \
    pip2 install ipython && \
    pip2 install scikit-image


RUN apt-get update -y && \
    apt-get --no-install-recommends -y install \
    autogen \
    libtool \
    libltdl-dev	


# Install Java

RUN apt-get install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

# Install tcsh

RUN apt-get update
RUN apt-get install tcsh

RUN apt-get install -y gnutls-bin

USER psr
# Java
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# PGPLOT
ENV PGPLOT_DIR /usr/lib/pgplot5
ENV PGPLOT_FONT /usr/lib/pgplot5/grfont.dat
ENV PGPLOT_INCLUDES /usr/include
ENV PGPLOT_BACKGROUND white
ENV PGPLOT_FOREGROUND black
ENV PGPLOT_DEV /xs

# Define home, psrhome, OSTYPE and create the directory
ENV HOME /home/psr
ENV PSRHOME /home/psr/software
ENV OSTYPE linux
RUN mkdir -p /home/psr/software
WORKDIR $PSRHOME


RUN wget --no-check-certificate https://www.imcce.fr/content/medias/recherche/equipes/asd/calceph/calceph-2.3.2.tar.gz && \
    tar -xvvf calceph-2.3.2.tar.gz -C $PSRHOME && \
    git clone https://git.code.sf.net/p/tempo/tempo && \




# PGPLOT
ENV PGPLOT_DIR="/usr/lib/pgplot5" \
    PGPLOT_FONT="/usr/lib/pgplot5/grfont.dat" \
    PGPLOT_INCLUDES="/usr/include" \
    PGPLOT_BACKGROUND="white" \
    PGPLOT_FOREGROUND="black" \
    PGPLOT_DEV="/xs"


# tempo
ENV TEMPO=$PSRHOME"/tempo" \
    PATH=$PATH:$PSRHOME"/tempo/bin"
WORKDIR $PSRHOME/tempo
RUN ./prepare && \
    ./configure --prefix=$PSRHOME/tempo && \
    make && \
    make install

# PRESTO 3
WORKDIR $PSRHOME
RUN git clone https://github.com/scottransom/presto.git 
ENV PRESTO=$PSRHOME"/presto" \
    PATH=$PATH:$PSRHOME"/presto/bin" \
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PSRHOME"/presto/lib" \
    PYTHONPATH=$PYTHONPATH:$PSRHOME"/presto/lib/python"


# Go to previous commit
WORKDIR $PRESTO 
RUN git checkout 280da5ef2198e1a8afcda5c9e83d27accd17412e


WORKDIR $PRESTO/src
#RUN make makewisdom
RUN make prep && \
    make -j $(nproc) && \
    make 
#    make mpi
WORKDIR $PRESTO
RUN pip2 install .
ENV PYTHONPATH $PYTHONPATH:/home/psr/software/presto/python/presto
RUN env | awk '{print "export ",$0}' >> $HOME/.profile

# PICS 
WORKDIR $HOME
RUN git clone https://github.com/zhuww/ubc_AI.git

WORKDIR $PSRHOME
RUN rm -rf ./*.bz2 ./*.gz ./*.xz ./*.ztar ./*.zip

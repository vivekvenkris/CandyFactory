FROM nvidia/cuda:10.2-devel-ubuntu16.04

RUN apt-get update && apt-get install -y build-essential git nano vim emacs

RUN git clone https://github.com/ewanbarr/dedisp.git && \
    cd dedisp &&\
    git checkout arch61 &&\
    make -j 32 && \
    make install

RUN git clone https://github.com/ewanbarr/peasoup.git && \
    cd peasoup && \
    git checkout dedisp_gulping &&\
    make -j 32 && \
    make install


FROM ubuntu:20.04

# Candidate filter install
RUN apt-get update && \
  apt-get install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update

RUN apt-get install -y build-essential git python3.6 python3.6-dev python3-pip python3.6-venv

# update pip
RUN python3.6 -m pip install pip --upgrade


# python3.6 packages for candidate filtering
RUN pip3.6 install pandas scipy numpy astropy scikit-learn matplotlib 


# Install candidate filter and make it executable
WORKDIR $HOME/software
RUN git clone https://github.com/prajwalvp/candidate_filter.git
ENV PYTHONPATH $PYTHONPATH:$HOME/software/candidate_filter/candidate_filter
ENV PATH $PATH:$HOME/software/candidate_filter/candidate_filter

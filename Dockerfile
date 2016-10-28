FROM andrewosh/binder-base

MAINTAINER Ruslan Burakov <vkuddai92@yandex.ru>

USER root

# Add dependency
# RUN apt-get update
# RUN apt-get purge python-requests
# RUN apt-get install python-requests python-pip

# USER main

# Install requirements for Python 2
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# toggle toolbar ON and notebook name ON
RUN jt -t grade3 -T -N

FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install xinetd -y
RUN apt-get install python2.7 -y
RUN chmod 633 /tmp
RUN useradd -m ctf
COPY ./share /home/Need_some_flags_2
COPY ./xinetd /etc/xinetd.d/xinetd
RUN chmod 755 /home/Need_some_flags_2/*
RUN chmod 755 /etc/xinetd.d/xinetd
CMD ["/usr/sbin/xinetd","-dontfork"]

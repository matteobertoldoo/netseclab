FROM debian:latest

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install netbase openbsd-inetd rsh-redone-server \
  && echo 'root:password' | chpasswd \
  && echo '192.168.107.102' > /root/.rhosts \
  && sed -i 's/^#<off># telnet/telnet/' /etc/inetd.conf

EXPOSE 513/tcp 514/tcp

CMD ["/usr/sbin/inetd", "-i"]

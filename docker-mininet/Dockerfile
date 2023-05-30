FROM ubuntu:20.04

USER root
WORKDIR /root

RUN set -x \
	&& PAG='iproute2 iputils-ping mininet net-tools openvswitch-switch openvswitch-testcontroller tcpdump vim' \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends $PAG \
	&& rm -rf /var/lib/apt/lists/* \

EXPOSE 6633 6653 6640

# CMD ["/etc/init.d/openvswitch-switch", "start"]

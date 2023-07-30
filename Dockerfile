FROM openjdk:22-jdk-bullseye
LABEL authors="Shaun Kruger"

WORKDIR /minecraft

ENV SCRIPTS=/scripts
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/scripts:/usr/local/openjdk-22/bin"

RUN apt-get update; \
    apt-get install -yq jq pigz tofrodos ; \
    apt-get clean ; \
    mkdir /scripts ; \
    wget -q https://github.com/Querz/mcaselector/releases/download/2.2.2/mcaselector-2.2.2.jar -O /scripts/mcaselector.jar

COPY scripts/* /scripts/

RUN chmod +x /scripts/*.py /scripts/*.sh ;\
    fromdos /scripts/*.py /scripts/*.sh ;\
    ln -s /scripts/* /usr/local/bin

CMD "/bin/bash"
#ENTRYPOINT ["/bin/bash"]
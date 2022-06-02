FROM apache/nifi:1.16.2
# change user so that image can be modified to install java11-jre and cypher-shell
USER root
RUN wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add -  && \
    echo 'deb https://debian.neo4j.com stable 4.4' | tee -a /etc/apt/sources.list.d/neo4j.list   && \
    apt-get update && \
    apt-get install -y openjdk-11-jre cypher-shell=1:4.4.4 && \
    apt-get -y autoremove && \
    apt-get -y clean
# change user back and update env vars to pick up jre 11
USER nifi
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=/usr/lib/jvm/java-11-openjdk-amd64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN java -version && \
    cypher-shell --version

FROM apache/nifi:1.16.2
# change user so that image can be modified to install java11-jre
USER root
RUN apt-get install -y openjdk-11-jre
# change user back and update env vars to pick up jre 11
USER nifi
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=/usr/lib/jvm/java-11-openjdk-amd64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN java -version

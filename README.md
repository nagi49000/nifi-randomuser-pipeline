# nifi-play
Play area for setting up nifi

The demo can be configured using
```
# in services
docker-compose build
```
followed by
```
# in services
docker-compose up
```
There may be some perms issues on the mount folders created by "docker-compose up"; if so, bring the services down, upgrade the perms on the created folders, and restart the services.

Access to the nifi and nifi-registry APIs can be verified by
```
curl http://localhost:18080/nifi-registry-api/access
curl http://localhost:8091/nifi-api/system-diagnostics
```

As an example, there is a docker image that will use nipyapi to set up a simple Nifi processor group (called "test_process_group_\<datetime\>"). This can be disabled in the docker-compose by removing the nipyapi docker block.

The nipyapi demo will create files containing "hello world", and put them in a folder called "/tmp/test_dst" in the nifi container. The files landing can be viewed by running
```
docker exec services_nifi_1 ls -aslFrt /tmp/test_dst/
```
which will peak at 100 files (and apply back-pressure through the Nifi flow, which should also be reported in the nifi logs).

The processor group (called "test_process_group_\<datetime\>") should be visible on nifi, by going to
```
http://localhost:8091/nifi/
```
You should be able to double click on the processor group, and explore the processors in the processor group (and see the files being generated and put).
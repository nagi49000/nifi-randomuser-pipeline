import time
import logging
from datetime import datetime
from nipyapi import config, canvas
import requests

logging.basicConfig(level=logging.DEBUG)

config.nifi_config.host = "http://nifi:8080/nifi-api"
config.registry_config.host = "http://registry:18080/nifi-registry-api"

status_code = 0
status_code_reg = 0
while status_code != 200 or status_code_reg != 200:
    try:
        status_code_reg = requests.get(config.registry_config.host + "/access").status_code
        logging.warning(f"status_code on /nifi-registry-api/access {status_code_reg}")
        status_code = requests.get(config.nifi_config.host + "/system-diagnostics").status_code
        logging.warning(f"status_code on /nifi-api/system-diagnostics {status_code}")
    except Exception as e:
        logging.warning(str(e))
    time.sleep(5)

logging.warning(f"Starting NiPyApi demo run, root_pg_id {canvas.get_root_pg_id()}")

# Example of building up processors with NiFi from
# https://community.cloudera.com/t5/Community-Articles/Building-Basic-Flows-with-Nipyapi/ta-p/270136

# location to visually place processor on canvas
location = (100, 200)

# send in configuration details for customizing the processors
processor_GenFlowFile_config = {
    "properties" : {
        "generate-ff-custom-text" : "hello world"
    },
    "schedulingPeriod" : "3 sec",
    "schedulingStrategy" : "TIMER_DRIVEN"
}
processor_PutFile_config = {
    "properties" : {
        "Directory" : "${dir}",
        "Conflict Resolution Strategy" : "replace",
        "Maximum File Count" : 100
    },
    "autoTerminatedRelationships" : ["failure", "success"]
}

# get the root processgroup ID
root_id = canvas.get_root_pg_id()

# get the root process group
root_process_group = canvas.get_process_group(root_id, "id")

# create the processor group
t = datetime.utcnow().isoformat(timespec="seconds") + "Z"
new_processor_group = canvas.create_process_group(root_process_group, f"test_process_group_{t}", location, f"this is a test created {t}")

# get the processors
processor_GenFlowFile = canvas.get_processor_type("org.apache.nifi.processors.standard.GenerateFlowFile", identifier_type="name")
processor_PutFile = canvas.get_processor_type("org.apache.nifi.processors.standard.PutFile", identifier_type="name")

# put processors on canvas in specificed process group
location = (900, 100)
GenFlowFile = canvas.create_processor(new_processor_group, processor_GenFlowFile, location, name=None, config=processor_GenFlowFile_config)
location = (100, 700)
PutFile = canvas.create_processor(new_processor_group, processor_PutFile, location, name=None, config=processor_PutFile_config)

# canvas create connection between processors
canvas.create_connection(GenFlowFile, PutFile, relationships=None, name="linkage")

# get variable registry
var_reg = canvas.get_variable_registry(new_processor_group, True)

# set new variables from incoming file
canvas.update_variable_registry(new_processor_group,([("dir", "/tmp/test_dst")]))

# start process group
canvas.schedule_process_group(new_processor_group.id, True)

logging.warning(f"demo files created: {dir()}")

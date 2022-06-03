import os
import time
import logging
from nipyapi import config, canvas
import requests

logging.basicConfig(level=logging.DEBUG)

neo4j_uri = "neo4j://neo4j:7687"
config.nifi_config.host = "http://nifi:8080/nifi-api"
config.registry_config.host = "http://registry:18080/nifi-registry-api"

# wait for nifi services to come up before deploying processors
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

# get the root processgroup ID
root_id = canvas.get_root_pg_id()

# get the root process group
root_process_group = canvas.get_process_group(root_id, "id")
proc_group_name = "randomuser_to_neo4j"

if proc_group_name in [x.component.name for x in canvas.list_all_process_groups()]:
    if os.getenv("NIFI_FORCE_PROCESSOR_CLEAN", "FALSE") == "TRUE":
        logging.warning(f"Processing group {proc_group_name} already exists; nuking it")
        proc_group = canvas.get_process_group(proc_group_name)
        canvas.delete_process_group(proc_group, force=True)
    else:
        logging.error(f"Processing group {proc_group_name} already exists; skipping deploying Nifi Flow")
        exit(0)

# create the processor group
location = (100, 200)  # location to visually place processor on canvas
proc_group = canvas.create_process_group(
    root_process_group, proc_group_name, location, f"take records from an api and put them in neo4j")

# set variables in the process group that will be used later on
canvas.update_variable_registry(proc_group, ([("success_put_file_dir", "/tmp/test_dst")]))
canvas.update_variable_registry(proc_group, ([("failure_put_file_dir", "/tmp/fail_to_parse")]))
canvas.update_variable_registry(proc_group, ([("neo4j_failure_put_file_dir", "/tmp/fail_neo4j_send")]))

# create controllers that will be used by processors within the processing group
# controllers and properties defined on https://nifi.apache.org/docs/nifi-docs/
# nipyapi's handling of controllers is lacking, so controllers configured using nifi's api
json_reader_name = "parser for randomuser json"
csv_writer_name = "write csv records"
controller_JsonTreeReader = canvas.get_controller_type("org.apache.nifi.json.JsonTreeReader")
controller_CSVRecordSetWriter = canvas.get_controller_type("org.apache.nifi.csv.CSVRecordSetWriter")
jsonTreeReader = canvas.create_controller(proc_group, controller_JsonTreeReader, name=json_reader_name)
csvRecordSetWriter = canvas.create_controller(proc_group, controller_CSVRecordSetWriter, name=csv_writer_name)

# modify the controllers directly using the nifi api, since nipyapi can't handle it
controllers_json = canvas.list_all_controllers(pg_id=root_id)
json_reader_uri = [x.uri for x in controllers_json if x.component.name == json_reader_name][0]
csv_writer_uri = [x.uri for x in controllers_json if x.component.name == csv_writer_name][0]
json_reader_id = [x.id for x in controllers_json if x.component.name == json_reader_name][0]
csv_writer_id = [x.id for x in controllers_json if x.component.name == csv_writer_name][0]
j = requests.get(json_reader_uri).json()
j["component"]["properties"]["starting-field-strategy"] = "NESTED_FIELD"
j["component"]["properties"]["starting-field-name"] = "results"
requests.put(json_reader_uri, json=j)

# get the processors
processor_FlattenJson = canvas.get_processor_type("org.apache.nifi.processors.standard.FlattenJson")
processor_ConvertRecord = canvas.get_processor_type("org.apache.nifi.processors.standard.ConvertRecord")
processor_MergeRecord = canvas.get_processor_type("org.apache.nifi.processors.standard.MergeRecord")
processor_InvokeHTTP = canvas.get_processor_type("org.apache.nifi.processors.standard.InvokeHTTP")
processor_PutFile = canvas.get_processor_type("org.apache.nifi.processors.standard.PutFile")
processor_ExecuteScript = canvas.get_processor_type("org.apache.nifi.processors.script.ExecuteScript")

# define a groovy script for an ExecuteScript processor to call
with open("csv-to-neo.groovy", "rt") as f:
    groovy_script = ''.join(f.readlines())

# send in configuration details for customizing the processors
# processors and properties defined on https://nifi.apache.org/docs/nifi-docs/
merge_record_name = "convert json to merged csv"
config_MergedRecord = {
    "properties": {
        "min-records": 10,
        "record-reader": json_reader_id,
        "record-writer": csv_writer_id
    },
    "autoTerminatedRelationships": ["original"]
}
config_FlattenJson = {
    "properties": {
        "flatten-json-separator": "_"
    }
}
config_InvokeHTTP = {
    "properties": {
        "Remote URL": "https://randomuser.me/api/"
    },
    "schedulingPeriod": "1 sec",
    "schedulingStrategy": "TIMER_DRIVEN"
}
config_merged_PutFile = {
    "properties": {
        "Directory": "${success_put_file_dir}",
        "Conflict Resolution Strategy": "replace",
        "Maximum File Count": 100
    },
    "autoTerminatedRelationships": ["failure"]
}
config_failure_PutFile = {
    "properties": {
        "Directory": "${failure_put_file_dir}",
        "Conflict Resolution Strategy": "replace",
        "Maximum File Count": 100
    },
    "autoTerminatedRelationships": ["failure", "success"]
}
config_ExecuteScript = {
    "properties": {
        "Script Engine": "Groovy",
        "Script File": None,
        "Script Body": groovy_script,
        "Module Directory": None,
        "neo4jUri": neo4j_uri
    },
    "autoTerminatedRelationships": ["success"]
}
config_neo4j_failure_PutFile = {
    "properties": {
        "Directory": "${neo4j_failure_put_file_dir}",
        "Conflict Resolution Strategy": "replace",
        "Maximum File Count": 100
    },
    "autoTerminatedRelationships": ["failure", "success"]
}

# put processors on canvas in specificed process group
invokeHTTP = canvas.create_processor(
    proc_group, processor_InvokeHTTP, location=(100, 100), name="get from randomuser api", config=config_InvokeHTTP
)
flattenJson = canvas.create_processor(
    proc_group, processor_FlattenJson, location=(100, 400), name="flatten deep json", config=config_FlattenJson
)
mergeRecord = canvas.create_processor(
    proc_group, processor_MergeRecord, location=(100, 700), name=merge_record_name, config=config_MergedRecord
)
success_putFile = canvas.create_processor(
    proc_group, processor_PutFile, location=(100, 1000), name="put file to disk", config=config_merged_PutFile
)
failure_putFile = canvas.create_processor(
    proc_group, processor_PutFile, location=(700, 700), name="failed jsons", config=config_failure_PutFile
)
neo4j_executeGroovyScript = canvas.create_processor(
    proc_group, processor_ExecuteScript, location=(100, 1300), name="send to neo4j", config=config_ExecuteScript
)
failure_neo4j_putFile = canvas.create_processor(
    proc_group, processor_PutFile, location=(700, 1300), name="failed to send to neo4j", config=config_neo4j_failure_PutFile
)

# canvas create connection between processors
canvas.create_connection(invokeHTTP, flattenJson, relationships=None, name="deep randomuser json")
canvas.create_connection(flattenJson, mergeRecord, relationships=None, name="flat randomuser json")
canvas.create_connection(mergeRecord, success_putFile, relationships=["merged"], name="merged randomuser csv")
canvas.create_connection(mergeRecord, failure_putFile, relationships=["failure"], name="failed randomuser json")
canvas.create_connection(success_putFile, neo4j_executeGroovyScript,
                         relationships=["success"], name="merged randomuser csv for neo4j")
canvas.create_connection(neo4j_executeGroovyScript, failure_neo4j_putFile,
                         relationships=["failure"], name="merged randomuser csvs neo4j failed")


# start the controllers and processor - using nipyapi's canvas.schedule_controller throws, so using nifi api directly
for uri in [json_reader_uri, csv_writer_uri]:
    j = requests.get(uri).json()
    j["component"]["state"] = "ENABLED"
    requests.put(uri, json=j)
# snooze a bit to wait for the controllers to start
wait_secs = 0
while (requests.get(json_reader_uri).json()["component"]["state"] != "ENABLED" and
       requests.get(csv_writer_uri).json()["component"]["state"] != "ENABLED" and
       wait_secs < 10):
    time.sleep(1)
    wait_secs += 1
# and then start the processor that uses the controllers
canvas.schedule_processor(mergeRecord, True)

# start process group
canvas.schedule_process_group(proc_group.id, True)

logging.warning(f"demo files created: {dir()}")

time.sleep(9999)

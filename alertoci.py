import sys
import os
import datetime
import oci

# OCI Settings
logOCID = "ocid1.log.oc1.eu-frankfurt-1.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
topicOCID = "ocid1.onstopic.oc1.eu-frankfurt-1.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Use parameter logonly, to only send alert to OCI Log and not send Notification
logonly = False
for a in sys.argv:
    if a.lower() == "logonly":
        logonly = True

# Get vSphere Alert information for environment settings
alarm_name = os.getenv('VMWARE_ALARM_NAME', 'debug_VMWARE_ALARM_NAME')
alarm_target_name = os.getenv('VMWARE_ALARM_TARGET_NAME', 'debug_VMWARE_ALARM_TARGET_NAME')
event_decscription = os.getenv('VMWARE_ALARM_EVENTDESCRIPTION', 'debug_VMWARE_ALARM_EVENTDESCRIPTION')
alarm_value = os.getenv('VMWARE_ALARM_ALARMVALUE', 'debug_VMWARE_ALARM_EVENTDESCRIPTION')
alarm_summary = os.environ.get("VMWARE_ALARM_TRIGGERINGSUMMARY", "debug_VMWARE_ALARM_TRIGGERINGSUMMARY")
alarm_vm = os.getenv('VMWARE_ALARM_EVENT_VM', 'debug_VMWARE_ALARM_EVENT_VM')
alarm_user = os.getenv('VMWARE_ALARM_EVENT_USERNAME', 'debug_VMWARE_ALARM_EVENT_USERNAME')

# Make sure you configure the OCI config file for authentication against OCI
configfile = "~/.oci/config"
config = oci.config.from_file(configfile)

# Send Alert information to OCI Log
loggingingestion_client = oci.loggingingestion.LoggingClient(config)
dt = datetime.datetime.now(datetime.timezone.utc)
put_logs_response = loggingingestion_client.put_logs(
    log_id=logOCID,
    put_logs_details=oci.loggingingestion.models.PutLogsDetails(
        specversion="1.0",
        log_entry_batches=[
            oci.loggingingestion.models.LogEntryBatch(
                entries=[
                    oci.loggingingestion.models.LogEntry(
                        data="{}\n{}\nVM: {}\nUser: {}".format(event_decscription,alarm_summary, alarm_vm, alarm_user),
                        id=alarm_target_name
                        )],
                source=alarm_target_name,
                type=alarm_name,
                defaultlogentrytime=dt.isoformat(),
                subject=alarm_name)]),
    opc_agent_version="vCenter Customer Log Agent",
    )

# Send Alert information as notification
if not logonly:
    ons = oci.ons.NotificationDataPlaneClient(config)
    msgDetails = oci.ons.models.MessageDetails()
    msgDetails.body = "vCenter Alarm:\n{}\n{}\n\nTarget: {},\nVM: {}\nUser: {}".format(event_decscription, alarm_summary, alarm_target_name, alarm_vm, alarm_user)
    msgDetails.title = "vCenter Alarm: {}".format(alarm_name)
    result = ons.publish_message(topic_id=topicOCID, message_details=msgDetails)



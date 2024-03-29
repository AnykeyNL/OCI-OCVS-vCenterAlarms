# OCI-OCVS-vCenterAlarms
Script for integrating OCVS vCenter Alarms to OCI Logging and notification services

## Installation instructions

### Install pip inside photonOS: (Be patient, it takes a few minutes)
tdnf install python3-pip

### Install OCI SDK, without touching any existing libraries
pip3 install -U --no-deps oci circuitbreaker

### Configure SDK to access OCI
mkdir /root/.oci
create config file: /root/.oci/config

Example:
[DEFAULT]
user=ocid1.user.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
fingerprint=ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff
key_file=/root/.oci/yourkeyfile.pem
tenancy=ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
region=eu-frankfurt-1

place key file in the right place, matching your config file

### Copy the alertoci.py script inside the vCenter server

mkdir /root/scripts
copy the contents into the script in that directory 

### Create or modify vCenter alarms. 

Add "run script":
/usr/bin/python /root/scripts/alertoci.py
![script example](https://github.com/AnykeyNL/OCI-OCVS-vCenterAlarms/raw/main/vcenter-alarm_example1.png)
or 
/usr/bin/python /root/scripts/alertoci.py logonly
![Script example](https://github.com/AnykeyNL/OCI-OCVS-vCenterAlarms/raw/main/vcenter-alarm_example2.png)


After this you will the triggered alarms in the OCI Logs service
![OCI Logs](https://github.com/AnykeyNL/OCI-OCVS-vCenterAlarms/raw/main/oci_logs_example.png)

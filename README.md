cisco_asr9k_cacti_cpu
=====================

Notes:
Script is written in python and tested on python 2.7.3.
Tested on cacti 0.8.7i
Tested on Cisco IOS-XR CRS-3 and ASR9010.
For snmp queries you need snmpwalk and snmpget installed.
By default snmp v2c is used.

- copy script_query_cisco_get_iosxr_cpu_stats.xml into CACTI_HOME/resource/script_queries/
- copy script_get_cisco_iosxr_cpu_stats.py into CACTI_HOME/scripts/
- through cacti web interface import templates: graph_data_template_cisco_iosxr_cpu_stats.xml and data_query_template_cisco_iosxr_cpu_stats.xml


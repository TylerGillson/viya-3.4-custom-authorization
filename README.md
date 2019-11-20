# Viya 3.4 Custom Authorization
A collection of scripts for generating custom authorization groups in SAS Viya 3.4.

# Overview
The generate_custom_authorization_groups.py script authorizes itself with a SAS Viya services node, then proceeds to programmatically generate custom Viya groups based on the contents of a custom group definition file. The group definition file's path is saved in config.py, but can also be specified at the command line.

The group definition file must be in CSV format and be structured as follows:

auto_group_name,group_1,group_2,...,group_n<br>
<custom_group_name>,<ldap_group_name>,<ldap_group_name>,...,<ldap_group_name><br>
...

For each row in the group definition file, the script will query the SAS Viya Identities REST API to accomplish the following:
  1. Determine the custom group's membership. This is the overall intersection of input group_1 through group_n, i.e. determine which members are in ALL of the input groups.
  2. Create the automatically maintained group if it does not already exist
  3. Add net-new members to the automatically maintained group
  4. Remove deprecated members from the automatically maintained group

# Usage
  - python generate_custom_authorization_groups.py [--options]

#
# Copyright © 2019, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# REST API CONSTANTS:
BASE_URL = "http://cantyg-full-viya.canpsd-fcc.sashq-d.openstack.sas.com"
OATH_TOKEN = None
DEFAULT_REST_KWARGS = {
    "data": None,
    "accept_type": "application/json",
    "content_type": "application/json"
}

# SAS-ADMIN CLI CONSTANTS:
CREDENTIALS_PATH = "C:\\Users\\cantyg\\.sas\\credentials.json"

# LDAP GROUP CUSTOMIZATION CONSTANTS:
CUSTOM_GROUPS_DEFINITION_FILE = "C:\\Users\\cantyg\\Downloads\\SA_AUTHORIZATION\\auto-maintained-groups.csv"

# LOGGING CONSTANTS:
LOG_ROOT = "C:\\Users\\cantyg\\Downloads\\SA_AUTHORIZATION"

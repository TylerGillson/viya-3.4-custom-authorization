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
import json
import requests
from custom_auth import config, logger
from custom_auth.oath_helper import get_oauth_token

"""
rest_api_helper.py
==================

A collection of helper methods for querying the SAS Identities API in order to: create custom groups,
verify the existence of custom groups, retrieve the members of existing LDAP groups, and manage the
membership of custom groups.
"""


def create_group(group_id, group_name):
    """
    Use the SAS Identities API to create a custom group object.

    Parameters:
        - group_id: The ID of the LDAP group being created.
        - group_name: The name of the LDAP group being created.
    """

    kwargs = config.DEFAULT_REST_KWARGS
    kwargs["data"] = {"id": group_id, "name": group_name}
    http_response = call_rest_api("/identities/groups/", "post", **kwargs)
    if http_response.status_code != 201:  # 201 = 'new group created'
        raise ValueError(http_response.text)
    logger.log(f"New custom group, {group_name}, with ID: {group_id}, was created successfully.")


def get_all_ldap_group_users(group_id):
    """
    Query the SAS Identities API to retrieve all users contained within an LDAP group object's member tree.

    Parameters:
        - group_id: The ID of the LDAP group to retrieve users from.

    Return:
        - users: A JSON array of user objects.
    """

    endpoint = f"/identities/groups/{group_id}/userMembers?depth=-1"  # recurse to bottom of LDAP group's member tree
    http_response = call_rest_api(endpoint, "get", **config.DEFAULT_REST_KWARGS)
    if http_response.status_code != 200:  # 200 = 'OK'
        raise ValueError(http_response.text)
    users = http_response.json()["items"]
    return users


def check_ldap_group_existence(group_id):
    """
    Query the SAS Identities API to determine if an LDAP group exists or not.

    Parameters:
        - group_id: The ID of the LDAP group of interest.

    Return:
        - A boolean flag.
    """
    endpoint = f"/identities/groups/{group_id}"
    http_response = call_rest_api(endpoint, "head", **config.DEFAULT_REST_KWARGS)
    if http_response.status_code == 200:  # 200 = 'OK. Group exists.'
        return True
    return False


def modify_group_membership(http_method, group_id, user_id):
    """
    Modify the membership of an existing group (LDAP or custom).

    Parameters:
        - http_method: Either 'put' or 'delete' for addition or deletion, respectively.
        - group_id: The ID of the group being modified.
        - user_id: The ID of the user being added or removed.
    """

    if http_method not in ["put", "delete"]:
        raise ValueError(f"Invalid HTTP request type: {http_method}")
    endpoint = f"/identities/groups/{group_id}/userMembers/{user_id}"
    http_response = call_rest_api(endpoint, http_method, **config.DEFAULT_REST_KWARGS)

    # Adding a user:
    if http_method == "put":
        if http_response.status_code != 201:  # 201 = 'member added to group'
            raise ValueError(http_response.text)
        logger.log(f"A user with ID: {user_id}, was added to the custom group with ID: {group_id}.")

    # Removing a user:
    elif http_method == "delete":
        if http_response.status_code != 204:  # 204 = 'member removed'
            raise ValueError(http_response.text)
        logger.log(f"A user with ID: {user_id}, was removed from the custom group with ID: {group_id}.")


def call_rest_api(request_value, request_type, **kwargs):
    """
    Execute an HTTP request against a SAS REST API. In this case, the API in question will always be the Identities API.

    Parameters:
        - request_value: An API endpoint.
        - request_type: An HTTP request type, i.e. 'get', 'put', 'head', etc.
        - kwargs: A dictionary of key-value pairs, including data, which contains the request body.

    Return:
        - The HTTP response from the API endpoint.
    """

    # Validate the HTTP request type:
    try:
        http_method = getattr(requests, request_type)
    except AttributeError as error:
        raise ValueError(repr(error))

    # Get keyword arguments:
    data = kwargs.pop("data", None)
    content_type = kwargs.pop("content_type", None)
    accept_type = kwargs.pop("accept_type", None)

    # Acquire a bearer token for the SAS Administration CLI:
    if config.OATH_TOKEN is None:
        config.OATH_TOKEN = get_oauth_token()

    # Build the authorization header and serialize the data string for the request to JSON format:
    head = {"Content-type": content_type, "Accept": accept_type, "Authorization": config.OATH_TOKEN}
    json_data = json.dumps(data, ensure_ascii=False)

    # Call the SAS Viya REST API:
    return http_method(config.BASE_URL + request_value, headers=head, data=json_data)

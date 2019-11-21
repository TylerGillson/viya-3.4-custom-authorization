from argument_helper import parse_arguments
from config import CUSTOM_GROUPS_DEFINITION_FILE
from rest_api_helper import create_group, get_all_ldap_group_users, check_ldap_group_existence, modify_group_membership


def main():
    """
    Usage:

        python generate_custom_authorization_groups.py [--options]

    Examples:

        1. Create and/or maintain auto-maintained groups from a group definition file specified at run-time:

            python generate_custom_authorization_groups.py -agf auto-groups.csv

        2. Same as above, but exercising all command-line options:

            python generate_custom_authorization_groups.py \
                --sas-endpoint http://cantyg-full-viya.canpsd-fcc.sashq-d.openstack.sas.com \
                --credentials-path C:\\Users\\cantyg\\.sas\\credentials.json \
                --auto-group-file C:\\Users\\cantyg\\Downloads\\SA_AUTHORIZATION\\auto-maintained-groups.csv
    """

    # Parse command-line arguments to update configuration at run-time:
    parse_arguments()

    # Read the auto-maintained groups file:
    with open(CUSTOM_GROUPS_DEFINITION_FILE, "r") as f:
        f.readline()  # Skip the file header
        auto_maintained_groups_raw = f.readlines()

    # Split each line up into its components & remove trailing characters:
    auto_maintained_groups = [l.strip().split(',') for l in auto_maintained_groups_raw]

    # Iterate over each line of the auto-maintained groups file:
    for group_definition in auto_maintained_groups:

        # Parse out auto-maintained group ID and input group ID(s):
        auto_group_name = group_definition[0]
        auto_group_id = group_definition[1]
        input_group_ids = group_definition[2:]

        # Determine if the auto-maintained group exists or not:
        auto_group_exists = check_ldap_group_existence(auto_group_id)

        # Get all users of the auto-maintained group if it exists:
        if auto_group_exists:
            auto_group_users = get_all_ldap_group_users(auto_group_id)
            auto_group_users = set([user["id"] for user in auto_group_users])

        # Otherwise, create it and initialize its users as an empty set:
        else:
            create_group(auto_group_id, auto_group_name)
            auto_group_users = set()

        # Iterate over all input groups and compute their combined intersection:
        input_users_intersection = set()
        for i, input_group_id in enumerate(input_group_ids):
            input_group_users = get_all_ldap_group_users(input_group_id)
            input_group_users = set([user["id"] for user in input_group_users])
            if i == 0:
                input_users_intersection = input_group_users
            else:
                input_users_intersection = input_group_users.intersection(input_users_intersection)

        # Determine target auto-maintained group membership:
        users_to_add = input_users_intersection.difference(auto_group_users)     # net-new users
        users_to_remove = auto_group_users.difference(input_users_intersection)  # deprecated users

        # Add/remove users to achieve target membership:
        list(map(lambda user_id: modify_group_membership("put", auto_group_id, user_id), users_to_add))
        list(map(lambda user_id: modify_group_membership("delete", auto_group_id, user_id), users_to_remove))


if __name__ == "__main__":
    main()

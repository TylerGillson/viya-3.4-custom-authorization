from config import DEFAULT_REST_KWARGS
from auth_and_rest_helpers import call_rest_api, parse_arguments


def get_group(group_name):
    endpoint = f"/identities/groups/?filter=startsWith(name,'{group_name}')"
    group = call_rest_api(endpoint, "get", **DEFAULT_REST_KWARGS)["items"]
    try:
        return group[0], True
    except IndexError:
        return None, False


def get_all_group_members(group_id):
    endpoint = f"/identities/groups/{group_id}/members?depth=-1"  # recurse to bottom of LDAP tree
    members = call_rest_api(endpoint, "get", **DEFAULT_REST_KWARGS)["items"]
    return members


def create_group(group_id, group_name):
    endpoint = f"/identities/groups/"
    kwargs = DEFAULT_REST_KWARGS
    kwargs["data"] = {
        "id": group_id,
        "name": group_name
    }
    call_rest_api(endpoint, "post", **kwargs)
    return get_group(group_name)


def modify_group_membership(http_method, group_id, member_id):
    endpoint = f"/identities/groups/{group_id}/groupMembers/{member_id}"
    call_rest_api(endpoint, http_method, **DEFAULT_REST_KWARGS)


def main():
    """
    Usage:
        python generate_custom_authorization_groups.py [--options]

    Examples:
        1. Build/re-build auto-maintained groups from a group definition file:
            python generate_custom_authorization_groups.py -agf auto-groups.csv
    """

    # Parse command-line arguments:
    auto_group_filename = parse_arguments()

    # Read the auto-maintained groups file:
    with open(auto_group_filename, "r") as f:
        f.readline()  # Skip the file header
        auto_maintained_groups_raw = f.readlines()

    # Split each line up into its components & remove trailing characters:
    auto_maintained_groups = [l.split(',')[0:-1] for l in auto_maintained_groups_raw]

    # Iterate over each line of the auto-maintained groups file:
    for group_data in auto_maintained_groups:

        # Parse out auto-maintained group name and input groups:
        auto_group_name = group_data[0]
        input_groups = group_data[1:]

        # Determine if the auto-maintained group exists or not:
        auto_group, auto_group_exists = get_group(auto_group_name)

        # Get all members of the auto-maintained group if it exists:
        if auto_group_exists:
            auto_group_members = get_all_group_members(auto_group["id"])
            auto_group_members = set([member["id"] for member in auto_group_members])

        # Otherwise, create it and initialize its members as an empty set:
        else:
            auto_group_id = auto_group_name.replace(" ", "-").lower()
            auto_group = create_group(auto_group_id, auto_group_name)
            auto_group_members = set()

        # Iterate over all input groups and compute their combined intersection:
        input_members_intersection = set()
        for i, input_group_name in enumerate(input_groups):
            input_group, _ = get_group(input_group_name)
            input_group_members = get_all_group_members(input_group["id"])
            input_group_members = set([member["id"] for member in input_group_members])
            if i == 0:
                input_members_intersection = input_group_members
            else:
                input_members_intersection = input_members_intersection.intersection(input_group_members)

        # Determine target auto-maintained group membership:
        members_to_add = input_members_intersection.difference(auto_group_members)     # net-new members
        members_to_remove = auto_group_members.difference(input_members_intersection)  # deprecated members

        # Add/remove members to achieve target membership:
        list(map(lambda member_id: modify_group_membership("put", auto_group, member_id), members_to_add))
        list(map(lambda member_id: modify_group_membership("delete", auto_group, member_id), members_to_remove))


if __name__ == "__main__":
    main()

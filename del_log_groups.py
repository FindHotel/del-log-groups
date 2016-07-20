#!/usr/bin/env python

"""Script helping to delete multiple AWS log groups at once."""

import argparse
import boto3


if __name__ == "__main__":

    # Argument definition
    parser = argparse.ArgumentParser(description="Delete several aws log "
                                     "groups at once. Always do a --dryrun "
                                     "before running it for real.")
    parser.add_argument(
            "log_group_prefix",
            type=str,
            help="all the log groups matching this prefix will be deleted "
    )
    parser.add_argument(
            "--dryrun",
            action="store_true",
            help="print the delete-log-group commands that would be executed "
    )
    args = parser.parse_args()

    client = boto3.client("logs")

    # Collect names of all the log groups matching the prefix
    log_groups = []
    response = client.describe_log_groups(
            logGroupNamePrefix=args.log_group_prefix,
    )
    log_groups += response["logGroups"]
    while "nextToken" in response:
        response = client.describe_log_groups(
                logGroupNamePrefix=args.log_group_prefix,
                nextToken=response["nextToken"]
        )
        log_groups += response["logGroups"]
    log_group_names = []
    for log_group in log_groups:
        log_group_names.append(log_group["logGroupName"])

    # Display or delete log groups according to the parameters given
    for log_group_name in log_group_names:
        print("aws logs delete-log-group --log-group-name " + log_group_name)
        if not args.dryrun:
            client.delete_log_group(logGroupName=log_group_name)

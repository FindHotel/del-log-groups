"""Script helping to delete multiple AWS log groups at once."""

import argparse
import boto3


# Argument definition
parser = argparse.ArgumentParser(description="Delete several aws log groups "
                                 "at once. Allways do a --dryrun before "
                                 "running it for real.")
parser.add_argument(
        "log_group_prefix",
        type=str,
        help="all the log groups matching this prefix will be deleted "
)
parser.add_argument(
        "--dryrun",
        action="store_true",
        help="print the log groups matching <log_group_prefix> "
        "without deleting them"
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
if args.dryrun:
    print("The log groups you are about to delete are:\n")
    for log_group_name in log_group_names:
        print(log_group_name)
else:
    for log_group_name in log_group_names:
        print("Deleting log group:  " + log_group_name)
        client.delete_log_group(logGroupName=log_group_name)

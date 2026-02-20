"""Health check utilities."""

import boto3
from botocore.exceptions import ClientError


def check_bedrock_access() -> tuple[bool, str]:
    """Check if Bedrock is accessible."""
    try:
        client = boto3.client("bedrock")
        # Try to list foundation models as a connectivity test
        client.list_foundation_models()
        return True, "Bedrock accessible"
    except ClientError as e:
        return False, f"Bedrock error: {str(e)}"
    except Exception as e:
        return False, f"Connection error: {str(e)}"


def check_aws_credentials() -> tuple[bool, str]:
    """Check if AWS credentials are configured."""
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        return True, f"Authenticated as {identity['Arn']}"
    except Exception as e:
        return False, f"Credentials error: {str(e)}"

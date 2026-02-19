"""Tests for health check utilities."""

import pytest
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from career_path.health import check_bedrock_access, check_aws_credentials


@patch('career_path.health.boto3.client')
def test_check_bedrock_access_success(mock_client):
    """Test successful Bedrock access check."""
    mock_bedrock = Mock()
    mock_bedrock.list_foundation_models.return_value = {}
    mock_client.return_value = mock_bedrock
    
    ok, msg = check_bedrock_access()
    assert ok is True
    assert "accessible" in msg.lower()


@patch('career_path.health.boto3.client')
def test_check_bedrock_access_client_error(mock_client):
    """Test Bedrock access check with ClientError."""
    mock_bedrock = Mock()
    mock_bedrock.list_foundation_models.side_effect = ClientError(
        {'Error': {'Code': 'AccessDenied', 'Message': 'Access denied'}},
        'ListFoundationModels'
    )
    mock_client.return_value = mock_bedrock
    
    ok, msg = check_bedrock_access()
    assert ok is False
    assert "Bedrock error" in msg


@patch('career_path.health.boto3.client')
def test_check_bedrock_access_general_error(mock_client):
    """Test Bedrock access check with general error."""
    mock_client.side_effect = Exception("Connection failed")
    
    ok, msg = check_bedrock_access()
    assert ok is False
    assert "Connection error" in msg


@patch('career_path.health.boto3.client')
def test_check_aws_credentials_success(mock_client):
    """Test successful AWS credentials check."""
    mock_sts = Mock()
    mock_sts.get_caller_identity.return_value = {
        'Arn': 'arn:aws:iam::123456789012:user/test'
    }
    mock_client.return_value = mock_sts
    
    ok, msg = check_aws_credentials()
    assert ok is True
    assert "Authenticated" in msg
    assert "arn:aws:iam" in msg


@patch('career_path.health.boto3.client')
def test_check_aws_credentials_error(mock_client):
    """Test AWS credentials check with error."""
    mock_client.side_effect = Exception("No credentials")
    
    ok, msg = check_aws_credentials()
    assert ok is False
    assert "Credentials error" in msg

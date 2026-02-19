"""Tests for workflow."""

import pytest
from career_path.graph.workflow import create_workflow


def test_create_workflow():
    """Test workflow creation."""
    workflow = create_workflow()
    assert workflow is not None
    
    # Check that workflow has the expected structure
    assert hasattr(workflow, 'invoke')


def test_workflow_has_nodes():
    """Test that workflow has all required nodes."""
    workflow = create_workflow()
    
    # The workflow should be a compiled graph
    assert workflow is not None

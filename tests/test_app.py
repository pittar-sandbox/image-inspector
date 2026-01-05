import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import json
import subprocess

# Add the project root to the python path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route returns 200 and renders the template."""
    # Since we can't easily check for template rendering without template context, 
    # we'll just check for status code 200.
    # In a real scenario, we might want to check for specific content in the response.
    response = client.get('/')
    assert response.status_code == 200

def test_inspect_image_missing_url(client):
    """Test that missing image_url returns 400."""
    response = client.post('/inspect', data={})
    assert response.status_code == 400
    assert b'Image URL is required' in response.data

@patch('subprocess.run')
def test_inspect_image_success(mock_subprocess, client):
    """Test successful image inspection."""
    # Mock the subprocess result
    mock_output = {
        'Layers': ['layer1', 'layer2'],
        'Digest': 'sha256:12345',
        'LayersData': [
            {'Size': 100},
            {'Size': 200}
        ],
        'Name': 'test-image',
        'Os': 'linux',
        'Architecture': 'amd64'
    }
    mock_process = MagicMock()
    mock_process.stdout = json.dumps(mock_output)
    mock_process.returncode = 0
    mock_subprocess.return_value = mock_process

    response = client.post('/inspect', data={'image_url': 'my-image'})
    
    assert response.status_code == 200
    assert response.json == mock_output
    
    # Verify subprocess was called correctly
    mock_subprocess.assert_called_once()
    args, _ = mock_subprocess.call_args
    cmd_args = args[0]
    assert 'skopeo' in cmd_args
    assert 'inspect' in cmd_args
    assert 'docker://my-image' in cmd_args

@patch('subprocess.run')
def test_inspect_image_with_params(mock_subprocess, client):
    """Test image inspection with OS and Architecture parameters."""
    mock_process = MagicMock()
    mock_process.stdout = "{}"
    mock_process.returncode = 0
    mock_subprocess.return_value = mock_process

    response = client.post('/inspect', data={
        'image_url': 'my-image',
        'os_type': 'linux',
        'architecture': 'amd64'
    })
    
    assert response.status_code == 200
    
    # Verify subprocess was called with correct flags
    mock_subprocess.assert_called_once()
    args, _ = mock_subprocess.call_args
    cmd_args = args[0]
    
    # Check for --override-os linux
    assert '--override-os' in cmd_args
    assert 'linux' in cmd_args
    
    # Check for --override-arch amd64
    assert '--override-arch' in cmd_args
    assert 'amd64' in cmd_args

@patch('subprocess.run')
def test_inspect_image_with_creds(mock_subprocess, client):
    """Test image inspection with credentials."""
    mock_process = MagicMock()
    mock_process.stdout = "{}"
    mock_process.returncode = 0
    mock_subprocess.return_value = mock_process

    response = client.post('/inspect', data={
        'image_url': 'private-image',
        'username': 'myuser',
        'password': 'mypassword'
    })
    
    assert response.status_code == 200
    
    # Verify subprocess was called with correct flags
    mock_subprocess.assert_called_once()
    args, _ = mock_subprocess.call_args
    cmd_args = args[0]
    
    # Check for --creds myuser:mypassword
    assert '--creds' in cmd_args
    assert 'myuser:mypassword' in cmd_args

@patch('subprocess.run')
def test_inspect_image_skopeo_error(mock_subprocess, client):
    """Test handling of skopeo command failure."""
    # Simulate CalledProcessError
    mock_subprocess.side_effect = subprocess.CalledProcessError(
        returncode=1, 
        cmd=['skopeo', 'inspect'], 
        stderr="image not found"
    )

    response = client.post('/inspect', data={'image_url': 'bad-image'})
    
    assert response.status_code == 500
    assert b'Failed to inspect image' in response.data
    assert b'image not found' in response.data

@patch('subprocess.run')
def test_inspect_image_json_error(mock_subprocess, client):
    """Test handling of invalid JSON from skopeo."""
    mock_process = MagicMock()
    mock_process.stdout = "Invalid JSON"
    mock_process.returncode = 0
    mock_subprocess.return_value = mock_process

    response = client.post('/inspect', data={'image_url': 'my-image'})
    
    assert response.status_code == 500
    assert b'Failed to parse skopeo output' in response.data

@patch('subprocess.run')
def test_inspect_image_with_spaces_success(mock_subprocess, client):
    """Test successful image inspection when URL has surrounding spaces."""
    # Mock the subprocess result
    mock_output = {
        'Layers': ['layer1'],
        'Name': 'test-image'
    }
    mock_process = MagicMock()
    mock_process.stdout = json.dumps(mock_output)
    mock_process.returncode = 0
    mock_subprocess.return_value = mock_process

    # Send URL with spaces
    response = client.post('/inspect', data={'image_url': ' my-image '})
    
    assert response.status_code == 200
    assert response.json == mock_output
    
    # Verify subprocess was called with STRIPPED URL
    mock_subprocess.assert_called_once()
    args, _ = mock_subprocess.call_args
    cmd_args = args[0]
    # Should contain 'docker://my-image' NOT 'docker:// my-image '
    assert 'docker://my-image' in cmd_args

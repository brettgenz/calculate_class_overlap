import os
import sys
import pytest
import tiktoken
from unittest.mock import patch, MagicMock

# Ensure the src folder is on the Python path
relative_path = os.path.abspath('.')
sys.path.append(relative_path)

from src.embedding_functions import *


def test_truncate_text_no_truncation():
    """Test that a short text is not modified."""
    text = "This is a short test."
    truncated = truncate_text(text, max_tokens=1000)
    assert truncated == text


def test_truncate_text_truncation():
    """Test that a long text is properly truncated to max_tokens."""
    text = "word " * 100  # Generate a long text
    max_tokens = 50
    truncated = truncate_text(text, max_tokens=max_tokens)
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(truncated)
    # Check that the number of tokens does not exceed max_tokens
    assert len(tokens) <= max_tokens


# @patch('embedding_functions.client')
# def test_get_embedding(mock_client):
#     """Test that get_embedding returns a dummy embedding."""
#     # Create a dummy embedding and configure the mock response
#     dummy_embedding = [0.1, 0.2, 0.3]
#     mock_response = MagicMock()
#     mock_obj = MagicMock()
#     mock_obj.embedding = dummy_embedding
#     mock_response.data = [mock_obj]
#     mock_client.embeddings.create.return_value = mock_response

#     text = "Test text for embedding."
#     result = get_embedding(text)

#     assert result == dummy_embedding
#     mock_client.embeddings.create.assert_called()

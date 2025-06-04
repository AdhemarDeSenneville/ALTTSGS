import pytest
from utils import split_text


def test_split_text_custom_pattern():
    text = "alpha?beta?gamma"
    result = split_text(text, min_length=1, max_length=100, split_pattern=r'\?')
    assert result == "alpha\nbeta\ngamma"


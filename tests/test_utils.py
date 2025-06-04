import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import split_text


def test_split_pattern_custom_regex():
    text = "alpha?beta?gamma"
    result = split_text(text, min_length=1, max_length=100, split_pattern=r'\?')
    assert result == "alpha\nbeta\ngamma"


def test_long_segments_split_and_short_segments_merged():
    text = (
        "small. This is a really long segment that should be split by spaces because it's too long. tiny."
    )
    result = split_text(text, min_length=10, max_length=20, split_pattern=r'\.')
    lines = result.split("\n")

    # a long segment should have been split into multiple lines
    assert len(lines) > 2

    # verify short segments were merged and are not standalone
    assert lines[0].startswith("small ")
    assert lines[-1] != "tiny" and "tiny" in lines[-1]


def test_return_type_and_format():
    text = "alpha?beta?gamma"
    result = split_text(text, min_length=1, max_length=100, split_pattern=r'\?')
    assert isinstance(result, str)
    assert result.split("\n") == ["alpha", "beta", "gamma"]

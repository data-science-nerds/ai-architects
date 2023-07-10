''' pytest -vvvv'''
import pytest
from your_module import decisions, parse_signed_value, cleanse_text  # Replace 'your_module' with your actual module name
from chatbot_things.data_handling.data_cleanse.make_priming import (
    strip_spaces_and_newlines_in_dict,
    decisions,
    parse_signed_value,
    cleanse_text,
)


# Parameterize the test_decisions
@pytest.mark.parametrize("input_str, expected_result", [
    ("1 this is correct OR 0 this is not", "1 this is correct"),
    ("2 this is also correct OR 0 this is not", "2 this is also correct"),
])
def test_decisions(input_str, expected_result):
    result = decisions(input_str)
    assert result['refund check'] == expected_result

# Parameterize the test_parse_signed_value
@pytest.mark.parametrize("input_dict, expected_result", [
    ({'signed': '1 this is correct OR 0 this is not'}, "1 this is correct"),
    ({'signed': '2 this is also correct OR 0 this is not'}, "2 this is also correct"),
])
def test_parse_signed_value(input_dict, expected_result):
    result = parse_signed_value(input_dict)
    assert result['signed']['refund check'] == expected_result

# Parameterize the test_cleanse_text
@pytest.mark.parametrize("input_txt, expected_result", [
    ("{'signed': '1 this is correct OR 0 this is not'}", "1 this is correct"),
    ("{'signed': '2 this is also correct OR 0 this is not'}", "2 this is also correct"),
])
def test_cleanse_text(input_txt, expected_result):
    result = cleanse_text(input_txt)
    assert result['signed']['refund check'] == expected_result


# Test cleanse_text function
def teststrip_spaces_and_newlines_in_dict():
    txt = "{'signed': '1 this is correct OR 0 this is not'}"
    result = strip_spaces_and_newlines_in_dict(txt)
    assert result['signed']['refund check'] == "1 this is correct"


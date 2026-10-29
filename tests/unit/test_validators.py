import argparse

import pytest

from etl.cli import create_parser
from etl.shared.validators import normalize_state_code


@pytest.mark.parametrize(
  ("value", "expected"),
  [("1", "01"), ("01", "01"), ("9", "09"), ("32", "32")],
)
def test_normalize_state_code_accepts_valid_codes(value: str, expected: str) -> None:
  assert normalize_state_code(value) == expected


@pytest.mark.parametrize("value", ["0", "33", "", "001", "1.0", "１２"])
def test_normalize_state_code_rejects_invalid_codes(value: str) -> None:
  with pytest.raises(argparse.ArgumentTypeError):
    normalize_state_code(value)


def test_create_parser_normalizes_state_and_parses_refresh() -> None:
  args = create_parser().parse_args(["--state", "1", "--refresh"])

  assert args.state == "01"
  assert args.refresh is True


def test_create_parser_defaults_to_all_states_and_cached_data() -> None:
  args = create_parser().parse_args([])

  assert args.state is None
  assert args.refresh is False

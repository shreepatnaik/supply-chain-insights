import pytest
from core.verify import check_proposal

def test_rejects_unknown_method():
    verdict, feedback = check_proposal("magic", None, {"naive": 4.3, "ets": 4.0}, None)
    assert verdict == "reject"
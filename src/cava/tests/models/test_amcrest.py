from cava.models.amcrest import event
import pytest
from pydantic import ValidationError


def test_amcrest_valid_json(amcrest_json):
    valid_amcrest = event(**amcrest_json)
    assert valid_amcrest.index == 1


def test_amcrest_invalid_json(amcrest_json):
    amcrest_json["index"] = "one"

    with pytest.raises(ValidationError):
        event(**amcrest_json)


def test_amcrest_ttl_return_int(amcrest_json):
    my_event = event(**amcrest_json)
    assert int(my_event.ttl())

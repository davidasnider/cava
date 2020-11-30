from cava.models.amcrest import event
import pytest
import pydantic


def test_amcrest_valid_json(amcrest_json):

    valid_amcrest = event(**amcrest_json)
    assert valid_amcrest.index == 1


def test_amcrest_ionvalid_json(amcrest_json):
    amcrest_json["index"] = "one"

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        event(**amcrest_json)

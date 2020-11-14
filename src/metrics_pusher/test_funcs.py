import funcs
import json


def test_is_valid_json():
    my_object = {
        "measurement": "test",
        "tags": {
            "tag1": "mystring",
            "tag2": "mystring2",
        },
        "time": "some_date_string",
        "fields": {"field1": 1, "field2": 2.4},
    }

    json_string = json.dumps(my_object)
    assert funcs.is_valid_json(json_string)


def test_is_not_valid_json():
    my_object = {
        "tags": {
            "tag1": "mystring",
            "tag2": "mystring2",
        },
        "time": "some_date_string",
        "fields": {"field1": 1, "field2": 2.4},
    }

    json_string = json.dumps(my_object)
    assert not funcs.is_valid_json(json_string)

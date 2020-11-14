import json
import jsonschema


def is_valid_json(json_string):

    # Define our schema
    schema_def = """
    {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Influx Measurement",
    "type": "object",
    "properties": {
        "measurement": {
            "type": "string"
        },
        "tags": {
            "type": "object",
            "patternProperties": {
                "^.*": { "type": "string" }
            }
        },
        "time": {
            "type": "string"
        },
        "fields": {
            "type": "object",
            "patternProperties": {
                "^.*": { "type": "number" }
            }
        }
    },
    "required": ["measurement", "time", "fields"]
    }
"""

    schema = json.loads(schema_def)
    received = json.loads(json_string)
    try:
        jsonschema.validate(received, schema)
        return True
    except jsonschema.exceptions.ValidationError as Error:
        print(
            f"Schema Validation Error: {Error.message}\nFull payload was: {json_string}"
        )
        return False

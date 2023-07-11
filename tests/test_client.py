from microbit_api import MicrobitClient

def test_pythonize():
    dict = {
        "CamelOne": True,
        "APIKey": "string",
        "nested": {
            "CamelTwo": False,
            "APIKeyTwo": 5
        }
    }

    valid_dict = {
        "camel_one": True,
        "api_key": "string",
        "nested": {
            "camel_two": False,
            "api_key_two": 5
        }
    }

    assert MicrobitClient.pythonize(dict) == valid_dict
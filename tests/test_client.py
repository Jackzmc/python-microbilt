from microbilt_api.client import MicrobiltClient
from unittest import TestCase 

def test_pythonize():
    dict = MicrobiltClient.pythonize({
        "CamelOne": True,
        "APIKey": "string",
        "nested": {
            "CamelTwo": False,
            "APIKeyTwo": 5
        }
    })

    valid_dict = {
        "camel_one": True,
        "api_key": "string",
        "nested": {
            "camel_two": False,
            "api_key_two": 5
        }
    }

    TestCase().assertDictEqual(dict, valid_dict)
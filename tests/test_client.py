from microbilt_api.client import MicrobiltClient, PRODUCTION_URL, NotAuthorized
from unittest import TestCase 
import pytest
from requests import HTTPError

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

def test_auth_err():
    client = MicrobiltClient(None, PRODUCTION_URL)
    with pytest.raises(NotAuthorized) as ex:
        client.ABAAcctVerification(None, None)

def test_ABA_fail():
    pass
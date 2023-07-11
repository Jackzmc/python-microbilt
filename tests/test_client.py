from microbilt_api.client import MicrobiltClient, PRODUCTION_URL, SANDBOX_URL, NotAuthorized
from unittest import TestCase 
import pytest
from requests import HTTPError
from dotenv import load_dotenv

load_dotenv()

API_URL = SANDBOX_URL

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
    with pytest.raises(NotAuthorized) as ex:
        client = MicrobiltClient("invalid", "invalid2", API_URL)

def test_ABA_fail():
    client = MicrobiltClient(None, None, API_URL)
    res = client.ABAAcctVerification('11103093', '19945192099')
    assert res['decision_info']['decision'][0]['decision_code'] == 'D'
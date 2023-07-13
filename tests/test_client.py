from microbilt_api.client import MicrobiltClient, PRODUCTION_URL, SANDBOX_URL, NotAuthorized
from unittest import TestCase 
import pytest
from requests import HTTPError
from dotenv import load_dotenv

load_dotenv()

API_URL = SANDBOX_URL

@pytest.fixture
def client():
    return MicrobiltClient(None, None, API_URL)

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
        MicrobiltClient("invalid", "invalid2", API_URL)

def test_ABA_fail(client: MicrobiltClient):
    res = client.ABAAcctVerification('11103093', '19945192099')
    assert res['decision_info']['decision'][0]['decision_code'] == 'D'

def test_ABA_succeed(client: MicrobiltClient):
    res = client.ABAAcctVerification('011103093', '9945192099')
    assert res['decision_info']['decision'][0]['decision_code'] == 'A'

    res = client.ABAAcctVerification('011103093', '19945192099')
    assert res['decision_info']['decision'][0]['decision_code'] == 'A'

# def test_addr_validate_fail(client):
#     res = client.AddressStandardization("1640 Airport Road #115", "Kennesaw", "GA", "30144")
#     print(res)

def test_addr_validate_succeed(client: MicrobiltClient):
    res = client.AddressStandardization("1640 Airport Road #115", "Kennesaw", "GA", "30144")
    assert res['msg_rs_hdr']['status']['status_code'] == 0
    assert res['post_addr']['street_name'] == 'AIRPORT'
    assert len(res['messages']) == 22
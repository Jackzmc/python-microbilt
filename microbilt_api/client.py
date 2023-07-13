import requests
from humps import decamelize
from os import environ
from datetime import datetime

PRODUCTION_URL = 'https://api.microbilt.com'
SANDBOX_URL = 'https://apitest.microbilt.com'

USER_AGENT = 'python-microbilt/v0.1.0'

class NotAuthorized(requests.HTTPError):
    """The apikey provided is not authorized or valid"""

class MicrobiltResponse:
    def __init__(self, json_response):
        """Takes in pythonized json data"""
        self.raw_response = json_response

    @property
    def data(self):
        return self.raw_response

    @property
    def response_data(self):
        return self.raw_response['msg_rs_hdr']
    
    @property
    def req_id(self):
        """Returns the ID of the request"""
        return self.raw_response['msg_rs_hdr']['rq_uid']
    
    @property
    def status(self):
        """Returns the status code of the request"""
        return self.raw_response['msg_rs_hdr']['status']['status_code']
    
    def __getitem__(self, key):
        return self.raw_response[key]
    
    def get_decisions(self):
        """Tries to parse the response's decision into a uniform decision"""
        decisions = []
        if 'response' in self.raw_response:
            code = self.raw_response['response']['decision']['decision']['code']
            value = self.raw_response['response']['decision']['decision']['Value']
            timestamp = datetime.strptime(self.raw_response['response']['decision']['decision_timestamp'], "%Y-%m-%d %H:%M:%S")
            decisions.append(MicrobiltDecision(code, value, timestamp))
        elif 'decision_info' in self.raw_response:
            for decision in self.raw_response['decision_info']['decision']:
                code = decision['decision_code']
                value = decision['text']
                timestamp = datetime.fromisoformat(decision['eff_dt'])
                decisions.append(MicrobiltDecision(code, value, timestamp))
        else:
            raise Exception("Could not find any decision object in response")
        return decisions

class MicrobiltDecision:
    def __init__(self, code, value, timestamp):
        self.code = code
        self.value = value
        self.timestamp = timestamp

class MicrobiltClient:
    """Creates a new MicrobiltCLient"""

    def pythonize(in_dict):
        return decamelize(in_dict)

    def __init__(self, client_id, client_secret, url = PRODUCTION_URL) -> None:
        """Creates a new API client

        :client_id
            the api client id, defaults to env variable MICROBILT_CLIENT_ID
        :client_secret
            the api client secret, defaults to env variable MICROBILT_CLIENT_SECRET
        :url
            the URL to make requests to, defaults to PRODUCTION_URL. Can be SANDBOX_URL
        """
        self._client_id = client_id or environ.get("MICROBILT_CLIENT_ID")
        self._client_secret = client_secret or environ.get("MICROBILT_CLIENT_SECRET")
        if self._client_id == None or self._client_secret == None:
            raise NotAuthorized("Invalid or missing client_id or client_secret")
        self.url = url.rstrip("/")
        self._get_token()

    def _get_url(self, append):
        return self.url + "/" + append
    
    def _get_token(self):
        res = requests.get(self._get_url('OAuth/GetAccessToken'), json={
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'client_credentials'
        })
        json = res.json()
        if 'fault' in json: raise Exception(json['fault']['faultstring'])
        if 'ErrorCode' in json: raise NotAuthorized(json['ErrorCode'] + ': ' + json['Error'])
        self._token = 'Bearer ' + json['access_token']
        print('got token')

    def _post_json(self, path, data = None, json = None) -> MicrobiltResponse:
        """Posts JSON and receives JSON that is automatically passed through Microbilt.pythonize
            Will also check for 401 unauthorized and send NotAuthorized
        """
        headers = {
            'Authorization': self._token,
            'User-Agent': USER_AGENT
        }
        res = requests.post(self._get_url(path), data=data, json=json, headers=headers)
        if res.status_code == 401:
            try:
                json = res.json()
                if 'fault' in json: raise NotAuthorized(json['fault']['faultstring'])
                if 'ErrorCode' in json: raise NotAuthorized(json['ErrorCode'] + ': ' + json['Error'])
            except requests.exceptions.JSONDecodeError:
                pass
            raise NotAuthorized(res.text)
        else:
            res.raise_for_status()
        return MicrobiltResponse(MicrobiltClient.pythonize(res.json()))

    

    def ABAAcctVerification(self, routing_number, account_number) -> MicrobiltResponse:
        """Performs a ABA account verification

        Example schema response: https://jsoneditoronline.org/#right=cloud.f4c062af787840bdaa44d144d48a2580&left=local.qaluxi
        (Will be pythonized)

        See https://developer.microbilt.com/api/ABAAcctVerification#/default/%2F for schemas (will be converted to snake case)
        """
        payload = {
            "BankRoutingNumber": routing_number,
            "BankAccountNumber": account_number
        }
        return self._post_json("ABAAcctVerification", json=payload)
    
    def AddressStandardization(self, address1: str, city: str, state: str, zip_code: str, address2: str = None, street_pre_dir: str = None, street_name: str = None, street_num: str = None, street_type: str = None, street_suffix: str = None, street_post_dir: str = None, country: str = None, county: str = None, apt: str = None) -> MicrobiltResponse:
        """Performs address validation and standardization

        Example schema response: https://jsoneditoronline.org/#right=cloud.f4c062af787840bdaa44d144d48a2580&left=local.qaluxi
        (Will be pythonized)

        See https://developer.microbilt.com/api/AddressStandardization#/default/%2F for schemas (will be converted to snake case)
        """
        payload = {
            'Address': {
                'Addr1': address1,
                'Addr2': address2,
                'StreetPreDir': street_pre_dir,
                'StreetName': street_name,
                'StreetNum': street_num,
                'StreetType': street_type,
                'StreetSuffix': street_suffix,
                'StreetPostDir': street_post_dir,
                'Apt': apt,
                'City': city,
                'State': state,
                'Zip': zip_code,
                'Country': country,
                'County': county
            }
        }
        return self._post_json("AddressStandardization", json=payload)
    
    def ACHCheckPrescreenLite(self) -> MicrobiltResponse:
        """Verifies bank routing numbers is valid and active (CA & US only), and check for validity of bank
        
        Example schema response: https://jsoneditoronline.org/#right=cloud.f4c062af787840bdaa44d144d48a2580&left=local.qaluxi
        (Will be pythonized)

        See https://developer.microbilt.com/api/ACHCheckPrescreenLite for schemas and more information
        """
        payload = {

        }
        raise NotImplemented("Not implemented")

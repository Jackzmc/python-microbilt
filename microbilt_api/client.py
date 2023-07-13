import requests
from humps import decamelize
from os import environ

PRODUCTION_URL = 'https://api.microbilt.com'
SANDBOX_URL = 'https://apitest.microbilt.com'

USER_AGENT = 'python-microbilt/v0.1.0'

class NotAuthorized(requests.HTTPError):
    """The apikey provided is not authorized or valid"""

class MicrobiltClient:
    """Creates a new MicrobiltCLient"""

    def pythonize(in_dict):
        return decamelize(in_dict)
        new_dict = dict()
        for key, val in in_dict.items():
            if type(val) == dict:
                new_dict[decamelize(key)] = MicrobiltClient.pythonize(val)
            elif hasattr(val, '__iter__'):
                for elem in val:
                    pythonize()
            else:
                new_dict[decamelize(key)] = val
        return new_dict

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

    def _post_json(self, path, data = None, json = None):
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
        return MicrobiltClient.pythonize(res.json())

    

    def ABAAcctVerification(self, routing_number, account_number):
        """Performs a ABA account verification

        See https://developer.microbilt.com/api/ABAAcctVerification#/default/%2F for schemas (will be converted to snake case)
        """
        payload = {
            "BankRoutingNumber": routing_number,
            "BankAccountNumber": account_number
        }
        return self._post_json("ABAAcctVerification", json=payload)
    
    def AddressStandardization(self, address1: str, city: str, state: str, zip_code: str, address2: str = None, street_pre_dir: str = None, street_name: str = None, street_num: str = None, street_type: str = None, street_suffix: str = None, street_post_dir: str = None, country: str = None, county: str = None, apt: str = None):
        """Performs address validation and standardization

        Example schema response: https://jsoneditoronline.org/#right=cloud.f4c062af787840bdaa44d144d48a2580&left=local.qaluxi
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
    
    

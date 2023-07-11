import requests
from humps import decamelize

PRODUCTION_URL = 'https://api.microbilt.com/'
SANDBOX_URL = 'https://apitest.microbilt.com/'

class NotAuthorized(requests.HTTPError):
    """The apikey provided is not authorized or valid"""

class MicrobiltClient:
    def pythonize(in_dict):
        new_dict = dict()
        for key, val in in_dict.items():
            if type(val) == dict:
                new_dict[decamelize(key)] = MicrobiltClient.pythonize(val)
            else:
                new_dict[decamelize(key)] = val
        return new_dict
    
    def _get_url(self, append):
        return self.url + "/" + append

    def __init__(self, apikey, url) -> None:
        self.apikey = apikey
        self.url = PRODUCTION_URL
    
    def ABAAcctVerification(self, routing_number, account_number):
        payload = {
            "BankRoutingNumber": routing_number,
            "BankAccountNumber": account_number
        }
        res = requests.post(self._get_url("ABAAcctVerification"), json=payload)  
        if res.status_code == 401:
            raise NotAuthorized()
        res.raise_for_status()  
        json = res.json()
        return MicrobiltClient.pythonize(json)
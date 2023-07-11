import requests
from humps import decamelize

PRODUCTION_URL = 'https://api.microbilt.com/'
SANDBOX_URL = 'https://apitest.microbilt.com/'

class MicrobiltClient:
    def pythonize(in_dict):
        new_dict = dict()
        for key, val in in_dict.items():
            if type(val) == dict:
                new_dict[decamelize(key)] = MicrobiltClient.pythonize(val)
            else:
                new_dict[decamelize(key)] = val
        return new_dict

    def __init__(self, apikey, url) -> None:
        self.apikey = apikey
        self.url = PRODUCTION_URL
    
    def ABAAcctVerification(self, routing_number, account_number):
        payload = {
            "BankRoutingNumber": routing_number,
            "BankAccountNumber": account_number
        }
        res = requests.post(self.url, json=payload)  
        res.raise_for_status()  
        json = res.json()
        return MicrobiltClient.pythonize(json)
        return {
            "ach_status": json.get("ACHStatus"),
            "change_date": json.get("ChangeDT"),
            "aba_number_schema": json.get("ABANumStatus"),
            "aba_number": json.get("ABANum"),
            "number_of_branches": json.get("NumOfBranches"),
            "branch_info": json.get("BranchInfo"),
            "decision_info": json.get("DecisionInfo")
        }
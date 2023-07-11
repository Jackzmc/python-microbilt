import requests
from humps import decamelize

PRODUCTION_URL = 'https://api.microbilt.com/'
SANDBOX_URL = 'https://apitest.microbilt.com/'

class MicrobitClient():
    def pythonize(dict):
        for key, val in dict.items():
            if type(val) == dict:
                dict[decamelize(key)] = MicrobitClient.pythonize(val)
            else:
                dict[decamelize(key)] = val
            del dict[key]
        return dict

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
        return MicrobitClient.pythonize(json)
        return {
            "ach_status": json.get("ACHStatus"),
            "change_date": json.get("ChangeDT"),
            "aba_number_schema": json.get("ABANumStatus"),
            "aba_number": json.get("ABANum"),
            "number_of_branches": json.get("NumOfBranches"),
            "branch_info": json.get("BranchInfo"),
            "decision_info": json.get("DecisionInfo")
        }
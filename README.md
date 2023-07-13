# python-microbilt

An unofficial, unsupported, work-in-progress API wrapper for Microbilt's APIs for python

See the tests for examples, no support will be given (I hate python)

Supported operations:

* **ABAAcctVerification**(self, routing_number, account_number)
* **AddressStandardization**(self, address1: str, city: str, state: str, zip_code: str, address2: str = None, street_pre_dir: str = None, street_name: str = None, street_num: str = None, street_type: str = None, street_suffix: str = None, street_post_dir: str = None, country: str = None, county: str = None, apt: str = None)
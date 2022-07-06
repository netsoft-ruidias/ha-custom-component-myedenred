DEFAULT_COUNTRY = "PT"

COUNTRIES = [
    { "value": DEFAULT_COUNTRY, "label": "Portugal" },
    { "value": "PO", "label": "Romania" },
]

API_LOGIN_URL = {
    "PT": "https://www.myedenred.pt/edenred-customer/api/authenticate/default",
    "RO": "https://myedenred.ro/edenred-customer/api/authenticate/default"
}

API_LIST_URL = {
    "PT": "https://www.myedenred.pt/edenred-customer/api/protected/card/list",
    "RO": "https://myedenred.ro/edenred-customer/api/protected/card/list",
}

API_ACCOUNTMOVEMENT_URL = {
    "PT": "https://www.myedenred.pt/edenred-customer/api/protected/card/{}/accountmovement",
    "RO": "https://myedenred.ro/edenred-customer/api/protected/card/{}/accountmovement",
}

"""
input:
{
    "amount": 25.73,
    "payorState": "NY",
    "collect": {
        "accountId": "123",
        "type": "ach"
    },
    "deliver": {
        "accountId": "456",
        "type": "virtualCard"
}

output:
[
{
    "amount": 25.73,
    "sourceAccountId": "123",
    "destinationAccountId": "melio-C",
    "paymentMethodType": "ach",
    "flow": "collect"
},
{
    "amount": 25.73,
    "sourceAccountId": "melio-C",
    "destinationAccountId": "456",
    "paymentMethodType": "virtualCard",
    "flow": "deliver"
}
]

Bank C is the only bank that can process payments delivered via Virtual Card
(“deliver.type == “virtualCard”)
Bank A is the only bank that can process payments originated from Texas (“payorState
== TX”)
Bank C is the only bank that can process international payments (“deliver.type ==
“international”)
Bank B is the only bank that can process check payments (“deliver.type == “check”)
after 15:00 (new Date().getHours() > 14).

"""
from email.policy import default
from typing import List, Dict
from datetime import datetime

BANKS = {
    'A': 'melio-A',
    'B': 'melio-B',
    'C': 'melio-C'
}

def _default_bank_chosser():
    # TBD
    return

def is_virtual_card(payment) -> str:
    if payment['deliver']['type'] == 'virtualCard':
        return BANKS['C']

def is_texas(payment) -> str:
    if payment['payorState'] == 'TX':
        return BANKS['A']

def is_international(payment) -> str:
    if payment['deliver']['type'] == 'international':
        return BANKS['C']

def is_check(payment) -> str:
    if payment['deliver']['type'] == 'check' and datetime.now() > datetime.now().replace(hour=15):
        return BANKS['B']


def _choose_bank_account(
        payment: Dict,
):
    for method in [
        is_virtual_card,
        is_texas,
        is_international,
        is_check
    ]:
        bank = method(payment)
        if bank:
            return bank

    return _default_bank_chosser()


def createTransfersForPayment(payment: Dict) -> List[Dict]:
    default_account_id = "melio"
    bank_account = _choose_bank_account(
        payment
      )

    return [
        {
            "amount": payment["amount"],
            "sourceAccountId": payment["collect"]["accountId"],
            "destinationAccountId": default_account_id,
            "paymentMethodType": payment["collect"]["type"],
            "flow": "collect"
        },
        {
            "amount": payment["amount"],
            "sourceAccountId": default_account_id,
            "destinationAccountId": payment["deliver"]["accountId"],
            "paymentMethodType": payment["deliver"]["type"],
            "flow": "deliver"
        }
    ]


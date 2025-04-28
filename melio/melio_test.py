from melio import createTransfersForPayment

input = {
    "amount": 25.73,
    "collect": {
        "accountId": "123",
        "type": "ach"
        },
    "deliver": {
        "accountId": "456",
        "type": "check"
    }
}

expected_output = [
    {
        "amount": 25.73,
        "sourceAccountId": "123",
        "destinationAccountId": "melio",
        "paymentMethodType": "ach",
        "flow": "collect"
    },
    {
        "amount": 25.73,
        "sourceAccountId": "melio",
        "destinationAccountId": "456",
        "paymentMethodType": "check",
        "flow": "deliver"
    }
]

output = createTransfersForPayment(input)
pprint(output)
assert output == expected_output
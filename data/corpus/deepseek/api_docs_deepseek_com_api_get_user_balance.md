<!-- source: https://api-docs.deepseek.com/api/get-user-balance -->
```
GET /user/balance
```

## /user/balance
Get user current balance

## Responses ​
- 200
OK, returns user balance info.
- application/json
- Schema
- Example
Schema
Whether the user's balance is sufficient for API calls.
balance_infos
object[]
- Array [
Array [
Possible values: CNY , USD
The currency of the balance.
The total available balance, including the granted balance and the topped-up balance.
The total not expired granted balance.
The total topped-up balance.
- ]
]
```
{ "is_available": true, "balance_infos": [ { "currency": "CNY", "total_balance": "110.00", "granted_balance": "10.00", "topped_up_balance": "100.00" } ] }
```

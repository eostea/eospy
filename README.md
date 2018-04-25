# eospy
Python library(wrapper) of the EOS.IO project.

As of before the June launch, this library is pretty much in flux. 
And there are some methods that have not been tested. Don't hold your breath. 

## Installation

You can install this package as usual with pip:

`pip install eospy`

## Example

### ChainApi

```python
from eospy import ChainApi


chain = ChainApi(hosts=['http://hk.party.eosfans.io:8888/', ])

# chain = ChainApi.local_network()

chain.get_info()
chain.get_block('5')
chain.get_account('eostea')

# More: https://eosio.github.io/eos/group__eosiorpc.html#chainrpc
```

### WalletApi

Not tested

```python
from eospy import WalletApi


wallet = WalletApi(hosts=['http://hk.party.eosfans.io:8888/', ])

# or wallet = WalletApi.local_network()

wallet.create('eostea')
wallet.open('eostea')

# More: https://eosio.github.io/eos/group__eosiorpc.html#walletrpc
```

## Exceptions
```python
from eospy.exceptions import BaseError

try:
    pass
    # something
except BaseError as err:
    print(err)

# All exceptions inherit from BaseError
```

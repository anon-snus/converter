from web3 import Web3
from web3.middleware import geth_poa_middleware

def get_private_from_seed(seed: str) -> str:
    web3 = Web3()
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    web3.eth.account.enable_unaudited_hdwallet_features()

    web3_account: LocalAccount = web3.eth.account.from_mnemonic(seed)

    private_key = web3_account._private_key.hex()
    address = web3_account.address
    return private_key, address


print("choose type: \n 1 - convert from seed \n 2 - convert from private keys \n 0 - exit ")
a = int(input())
if a==1:
    try:
        web3 = Web3()

        with open('privatekeys-seed.txt') as f:
            p_keys = f.read().splitlines()

        data = {}
        for seed in p_keys:
            pk, address = get_private_from_seed(seed)
            data[address] = pk

        with open('addresses.txt', 'a+') as f:
            for address, pk in data.items():
                f.write(f'{address}: {pk}\n')

        print(f'Converted {len(p_keys)} privatekeys')
    except Exception as err:
        print(f'ERROR: {err}')

    input('\n > Exit')
elif a==2:
    try:
        web3 = Web3()

        with open('privatekeys-seed.txt') as f:
            p_keys = f.read().splitlines()

        data = {}
        for pk in p_keys:
            acc = web3.eth.account.from_key(pk)
            data[acc.address] = pk

        with open('addresses.txt', 'a+') as f:
            for address, pk in data.items():
                f.write(f'{address}: {pk}\n')

        print(f'Converted {len(p_keys)} privatekeys')
    except Exception as err:
        print(f'ERROR: {err}')

    input('\n > Exit')
else:
    print('Exit')

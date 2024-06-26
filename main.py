from web3 import Web3

import csv

def get_private_from_seed(seed: str) -> tuple:
    web3 = Web3()
    web3.eth.account.enable_unaudited_hdwallet_features()

    web3_account = web3.eth.account.from_mnemonic(seed)

    private_key = web3_account._private_key.hex()
    address = web3_account.address
    return private_key, address


print("choose type: \n 1 - convert from seed \n 2 - convert from private keys \n 0 - exit ")
a = int(input())
if a == 1:
    try:
        web3 = Web3()

        with open('privatekeys-seed.txt') as f:
            p_keys = f.read().splitlines()

        data = []
        for seed in p_keys:
            pk, address = get_private_from_seed(seed)
            data.append((Web3.to_checksum_address(address), pk, seed))

        with open('addresses.csv', 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Address", "Private Key", "Seed"])
            writer.writerows(data)

        print(f'Converted {len(p_keys)} privatekeys')
    except Exception as err:
        print(f'ERROR: {err}')

    input('\n > Exit')
elif a == 2:
    try:
        web3 = Web3()

        with open('privatekeys-seed.txt') as f:
            p_keys = f.read().splitlines()

        data = []
        for pk in p_keys:
            if not pk.startswith('0x'):
                pk='0x'+pk
            acc = web3.eth.account.from_key(pk)
            data.append((Web3.to_checksum_address(acc.address), pk))

        with open('addresses.csv', 'a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Address", "Private Key"])
            writer.writerows(data)

        print(f'Converted {len(p_keys)} privatekeys')
    except Exception as err:
        print(f'ERROR: {err}')

    input('\n > Exit')
else:
    print('Exit')

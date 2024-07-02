import os
from web3 import Web3
import csv

def get_private_from_seed(seed: str) -> tuple:
    web3 = Web3()
    web3.eth.account.enable_unaudited_hdwallet_features()

    web3_account = web3.eth.account.from_mnemonic(seed)

    private_key = web3_account._private_key.hex()
    address = web3_account.address
    return private_key, address

def get_unique_filename(directory: str, base_filename: str) -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)
    base_path = os.path.join(directory, base_filename)
    filename, extension = os.path.splitext(base_path)
    counter = 1
    new_filename = f"{filename}{extension}"
    while os.path.exists(new_filename):
        new_filename = f"{filename}_{counter}{extension}"
        counter += 1
    return new_filename


try:
    web3 = Web3()

    with open('privatekeys-seed.txt') as f:
        p_keys = f.read().splitlines()

    data = []
    for seed in p_keys:
        if len(str(seed))<70:
            if seed[:2]!='0x':
                seed='0x'+seed
            acc = web3.eth.account.from_key(seed)
            data.append((Web3.to_checksum_address(acc.address), seed))
        else:

            pk, address = get_private_from_seed(seed)
            data.append((Web3.to_checksum_address(address), pk))

    results_dir='results'
    output_file = get_unique_filename(results_dir, 'addresses.csv')

    with open(output_file, 'a+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Address", "Private Key"])
        writer.writerows(data)

    print(f'Converted {len(p_keys)} private keys/seeds. Results saved in {output_file}')
except Exception as err:
    print(f'ERROR: {err}')


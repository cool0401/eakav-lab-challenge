from web3 import Web3

def get_ethereum_balance(address):
    alchemy_url = 'https://mainnet.infura.io/v3/4e1bcabefe5a4d86b9534ce4ef47e9e6'
    web3 = Web3(Web3.HTTPProvider(alchemy_url))

    if not web3.is_connected():
        return None

    checksum_address = web3.to_checksum_address(address)
    balance_wei = web3.eth.get_balance(checksum_address)
    balance_eth = web3.from_wei(balance_wei, 'ether')
    return balance_eth


def validate_ethereum_address(address):
    try:
        Web3.to_checksum_address(address)
        return True
    except ValueError:
        return False
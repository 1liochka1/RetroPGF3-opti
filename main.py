import random
from web3 import Web3
import time
from loguru import logger
from tqdm import tqdm
from eth_abi import *
from eth_utils import *
import pandas as pd
from config import DELAY, keys

abi = [{"inputs": [{"components": [{"internalType": "address", "name": "target", "type": "address"},
                                   {"internalType": "bytes", "name": "callData", "type": "bytes"}],
                    "internalType": "struct Multicall3.Call[]", "name": "calls", "type": "tuple[]"}],
        "name": "aggregate", "outputs": [{"internalType": "uint256", "name": "blockNumber", "type": "uint256"},
                                         {"internalType": "bytes[]", "name": "returnData", "type": "bytes[]"}],
        "stateMutability": "payable", "type": "function"}, {"inputs": [{"components": [
    {"internalType": "address", "name": "target", "type": "address"},
    {"internalType": "bool", "name": "allowFailure", "type": "bool"},
    {"internalType": "bytes", "name": "callData", "type": "bytes"}], "internalType": "struct Multicall3.Call3[]",
                                                                        "name": "calls", "type": "tuple[]"}],
                                                            "name": "aggregate3", "outputs": [{"components": [
        {"internalType": "bool", "name": "success", "type": "bool"},
        {"internalType": "bytes", "name": "returnData", "type": "bytes"}], "internalType": "struct Multicall3.Result[]",
                                                                                               "name": "returnData",
                                                                                               "type": "tuple[]"}],
                                                            "stateMutability": "payable", "type": "function"}, {
           "inputs": [{"components": [{"internalType": "address", "name": "target", "type": "address"},
                                      {"internalType": "bool", "name": "allowFailure", "type": "bool"},
                                      {"internalType": "uint256", "name": "value", "type": "uint256"},
                                      {"internalType": "bytes", "name": "callData", "type": "bytes"}],
                       "internalType": "struct Multicall3.Call3Value[]", "name": "calls", "type": "tuple[]"}],
           "name": "aggregate3Value", "outputs": [{"components": [
        {"internalType": "bool", "name": "success", "type": "bool"},
        {"internalType": "bytes", "name": "returnData", "type": "bytes"}], "internalType": "struct Multicall3.Result[]",
                                                   "name": "returnData", "type": "tuple[]"}],
           "stateMutability": "payable", "type": "function"}, {"inputs": [{"components": [
    {"internalType": "address", "name": "target", "type": "address"},
    {"internalType": "bytes", "name": "callData", "type": "bytes"}], "internalType": "struct Multicall3.Call[]",
                                                                           "name": "calls", "type": "tuple[]"}],
                                                               "name": "blockAndAggregate", "outputs": [
        {"internalType": "uint256", "name": "blockNumber", "type": "uint256"},
        {"internalType": "bytes32", "name": "blockHash", "type": "bytes32"}, {
            "components": [{"internalType": "bool", "name": "success", "type": "bool"},
                           {"internalType": "bytes", "name": "returnData", "type": "bytes"}],
            "internalType": "struct Multicall3.Result[]", "name": "returnData", "type": "tuple[]"}],
                                                               "stateMutability": "payable", "type": "function"},
       {"inputs": [], "name": "getBasefee",
        "outputs": [{"internalType": "uint256", "name": "basefee", "type": "uint256"}], "stateMutability": "view",
        "type": "function"},
       {"inputs": [{"internalType": "uint256", "name": "blockNumber", "type": "uint256"}], "name": "getBlockHash",
        "outputs": [{"internalType": "bytes32", "name": "blockHash", "type": "bytes32"}], "stateMutability": "view",
        "type": "function"}, {"inputs": [], "name": "getBlockNumber",
                              "outputs": [{"internalType": "uint256", "name": "blockNumber", "type": "uint256"}],
                              "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getChainId",
                                                                               "outputs": [{"internalType": "uint256",
                                                                                            "name": "chainid",
                                                                                            "type": "uint256"}],
                                                                               "stateMutability": "view",
                                                                               "type": "function"},
       {"inputs": [], "name": "getCurrentBlockCoinbase",
        "outputs": [{"internalType": "address", "name": "coinbase", "type": "address"}], "stateMutability": "view",
        "type": "function"}, {"inputs": [], "name": "getCurrentBlockDifficulty",
                              "outputs": [{"internalType": "uint256", "name": "difficulty", "type": "uint256"}],
                              "stateMutability": "view", "type": "function"},
       {"inputs": [], "name": "getCurrentBlockGasLimit",
        "outputs": [{"internalType": "uint256", "name": "gaslimit", "type": "uint256"}], "stateMutability": "view",
        "type": "function"}, {"inputs": [], "name": "getCurrentBlockTimestamp",
                              "outputs": [{"internalType": "uint256", "name": "timestamp", "type": "uint256"}],
                              "stateMutability": "view", "type": "function"},
       {"inputs": [{"internalType": "address", "name": "addr", "type": "address"}], "name": "getEthBalance",
        "outputs": [{"internalType": "uint256", "name": "balance", "type": "uint256"}], "stateMutability": "view",
        "type": "function"}, {"inputs": [], "name": "getLastBlockHash",
                              "outputs": [{"internalType": "bytes32", "name": "blockHash", "type": "bytes32"}],
                              "stateMutability": "view", "type": "function"}, {
           "inputs": [{"internalType": "bool", "name": "requireSuccess", "type": "bool"}, {
               "components": [{"internalType": "address", "name": "target", "type": "address"},
                              {"internalType": "bytes", "name": "callData", "type": "bytes"}],
               "internalType": "struct Multicall3.Call[]", "name": "calls", "type": "tuple[]"}], "name": "tryAggregate",
           "outputs": [{"components": [{"internalType": "bool", "name": "success", "type": "bool"},
                                       {"internalType": "bytes", "name": "returnData", "type": "bytes"}],
                        "internalType": "struct Multicall3.Result[]", "name": "returnData", "type": "tuple[]"}],
           "stateMutability": "payable", "type": "function"}, {
           "inputs": [{"internalType": "bool", "name": "requireSuccess", "type": "bool"}, {
               "components": [{"internalType": "address", "name": "target", "type": "address"},
                              {"internalType": "bytes", "name": "callData", "type": "bytes"}],
               "internalType": "struct Multicall3.Call[]", "name": "calls", "type": "tuple[]"}],
           "name": "tryBlockAndAggregate",
           "outputs": [{"internalType": "uint256", "name": "blockNumber", "type": "uint256"},
                       {"internalType": "bytes32", "name": "blockHash", "type": "bytes32"}, {
                           "components": [{"internalType": "bool", "name": "success", "type": "bool"},
                                          {"internalType": "bytes", "name": "returnData", "type": "bytes"}],
                           "internalType": "struct Multicall3.Result[]", "name": "returnData", "type": "tuple[]"}],
           "stateMutability": "payable", "type": "function"}]

wallets = []
results = []
def sleep_indicator(secs):
    for i in tqdm(range(secs), desc='жду', bar_format="{desc}: {n_fmt}c /{total_fmt}c {bar}", colour='green'):
        time.sleep(1)
def check_status_tx(tx_hash, address, w3):
    logger.info(f'{address} - жду подтверждения транзакции : https://optimistic.etherscan.io/tx/{to_hex(tx_hash)}...')

    start_time = int(time.time())
    while True:
        current_time = int(time.time())
        if current_time >= start_time + 100:
            logger.info(
                f'{address} - транзакция не подтвердилась за 100 cекунд, начинаю повторную отправку...')
            return 0
        try:
            status = w3.eth.get_transaction_receipt(tx_hash)['status']
            if status == 1:
                return status
            time.sleep(1)
        except Exception as error:
            time.sleep(1)
def check_nft(address):
    w3 = Web3(Web3.HTTPProvider('https://optimism.publicnode.com'))
    nft = Web3.to_checksum_address('0xd89dBBd35C24E07C7727BF1eF36cd1F02aEA158E')
    abi = '[{"inputs":[{"internalType":"address","name":"punkContract","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"address","name":"proxy","type":"address"}],"name":"ProxyRegistered","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"punkIndex","type":"uint256"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"punkIndex","type":"uint256"}],"name":"mint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"proxyInfo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"punkContract","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"registerProxy","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"baseUri","type":"string"}],"name":"setBaseURI","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
    contract = w3.eth.contract(address=nft, abi=abi)
    id = contract.functions.balanceOf(address).call()
    if id == 1:
        logger.info(f'{address} на кошельке уже есть RetroPGF 3 NFT...')
        return False
    else:
        return True


def mint(privatekey, delay):
    w3 = Web3(Web3.HTTPProvider('https://optimism.publicnode.com'))
    account = w3.eth.account.from_key(privatekey)
    address = account.address
    id_ = check_nft(address)
    to = Web3.to_checksum_address('0xca11bde05977b3631167028862be2a173976ca11')

    mint_data = to_bytes(hexstr=f'0x40c10f19{encode(["address", "uint256"], (address, 1)).hex()}')
    args = [
        {
        "target": Web3.to_checksum_address('0xd89dBBd35C24E07C7727BF1eF36cd1F02aEA158E'),
        "allowFailure": False,
        "callData": mint_data,
        "value": 0
    },
        {
            "target": Web3.to_checksum_address('0xAcCC1fe6537eb8EB56b31CcFC48Eb9363e8dd32E'),
            "allowFailure": False,
            "callData": "0x",
            "value": 440000000000000
    }
    ]

    multicall_contract = w3.eth.contract(address=to, abi=abi)

    if id_:
        logger.info(f'{address} - начинаю минт RetroPGF 3...')
        try:
            tx = multicall_contract.functions.aggregate3Value(args).build_transaction({
                'from': address,
                'nonce': w3.eth.get_transaction_count(address),
                'value': 440000000000000,
                'gas': multicall_contract.functions.aggregate3Value(args).estimate_gas({'from': address,
                                                                                        'nonce': w3.eth.get_transaction_count(address),
                                                                                        'value': 440000000000000, }),
                'maxFeePerGas': int(w3.eth.gas_price * 1.2),
                'maxPriorityFeePerGas': int(w3.eth.gas_price)
            })
            sign = account.sign_transaction(tx)
            hash_ = w3.eth.send_raw_transaction(sign.rawTransaction)
            status = check_status_tx(hash_, address, w3)
            sleep_indicator(5)
            if status == 1:
                logger.success(f'{address} - успешно заминтил RetroPGF 3 : https://optimistic.etherscan.io/tx/{to_hex(hash_)}...')
                sleep_indicator(random.randint(delay[0], delay[1]))
                return address, 'success'
            else:
                logger.info(f'{address} - пробую еще раз..')
                return mint(privatekey, delay)

        except Exception as e:
            logger.error(f'{address} - {e}')
            sleep_indicator(random.randint(delay[0], delay[1]))
            return address, 'error'

    else:
        return address, 'already minted'


def main():
    print(f'\n{" " * 32}автор - https://t.me/iliocka{" " * 32}\n')
    for key in keys:
        res = mint(key, DELAY)
        wallets.append(res[0]), results.append(res[1])
    res = {'address': wallets, 'result': results}
    df = pd.DataFrame(res)
    df.to_csv('results.csv', mode='a', index=False)
    logger.success('mинетинг закончен...')
    print(f'\n{" " * 32}автор - https://t.me/iliocka{" " * 32}\n')
    print(f'\n{" " * 32}donate - EVM 0xFD6594D11b13C6b1756E328cc13aC26742dBa868{" " * 32}\n')
    print(f'\n{" " * 32}donate - trc20 TMmL915TX2CAPkh9SgF31U4Trr32NStRBp{" " * 32}\n')

if __name__ == '__main__':
    main()

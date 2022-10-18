from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
DEVELOPMENT_ENVIRONMENTS = ["development", "ganache-local"]
DECIMALS = 8
STARTING_VALUE = 200000000000


def get_account():
    if (
        network.show_active() in DEVELOPMENT_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_verification_req_status():
    return config["networks"][network.show_active()]["verify"]


def get_priceFeed_address():
    if network.show_active() not in DEVELOPMENT_ENVIRONMENTS:
        return config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        return MockV3Aggregator[-1].address


def deploy_mocks():
    print("Deploying Mock Aggregator...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_VALUE, {"from": get_account()})
    print(f"Deployed mock aggregator at {MockV3Aggregator[-1].address}")

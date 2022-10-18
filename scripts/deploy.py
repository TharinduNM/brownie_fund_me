from brownie import FundMe
from scripts.util_scripts import (
    get_account,
    get_priceFeed_address,
    get_verification_req_status,
)


def deploy_fund_me():
    account = get_account()
    price_feed_address = get_priceFeed_address()
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=get_verification_req_status(),
    )
    print(f"Contract deployed at: {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()

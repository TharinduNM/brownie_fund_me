from brownie import FundMe, accounts

from scripts.util_scripts import get_account


def fund():
    account = get_account()
    fundme = FundMe[-1]
    entry_fee = fundme.getEntryFee()
    print(f"entrance fee = {entry_fee}")
    fundme.fund({"from": account, "value": entry_fee * 2})
    print(fundme.getUSDPriceOfEth())
    print(fundme.getValueOfEth(1))


def main():
    fund()

from brownie import FundMe, accounts
from scripts.util_scripts import get_account


def withdraw():
    fundme = FundMe[-1]
    account = get_account()
    fundme.withdraw({"from": account})


def main():
    withdraw()

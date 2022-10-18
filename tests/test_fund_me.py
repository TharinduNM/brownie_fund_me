from scripts.deploy import deploy_fund_me
from scripts.util_scripts import get_account, DEVELOPMENT_ENVIRONMENTS
from brownie import network, accounts, exceptions
import pytest


def test_deploy_fund_me():
    print("Running test ... test_deploy_fund_me...")
    fundme = deploy_fund_me()
    account = get_account()
    entrance_fee = fundme.getEntryFee()
    tx1 = fundme.fund({"from": account, "value": entrance_fee * 2})
    tx1.wait(1)
    assert fundme.addressOfFunder(account.address) == entrance_fee * 2
    tx2 = fundme.withdraw({"from": account})
    tx2.wait(1)
    assert fundme.addressOfFunder(account.address) == 0


def test_only_owner_can_withdraw():
    print("Running test.... only_owner_can_withdraw...")
    if network.show_active() not in DEVELOPMENT_ENVIRONMENTS:
        pytest.skip("only for local netrowks")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})

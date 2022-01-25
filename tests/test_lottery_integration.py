from brownie import Lottery, network, config
from scripts.helpful_scripts import *
from scripts.deploy_lottery import *
import pytest
import time


def test_can_pick_winner():
    skip_integration_test()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(300)
    assert lottery.recent_winner() == account
    assert lottery.balance() == 0

# 0.02 eth
# 200_000_000_000
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import *
from scripts.helpful_scripts import *
from web3 import Web3
import pytest

# Unit tests - way to test small pieces of code in an isolated instance (local env)
# Integration tests - testing accross multiple complex systems (testnet)
def test_get_entrance_fee():
    # if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    #     pytest.skip()
    skip_unit_test()
    # Arrange
    lottery = deploy_lottery()
    # Act
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    # Arrange
    skip_unit_test()
    lottery = deploy_lottery()
    # Act/Assert
    # should_revert(
    #     lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
    # )
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # Arrange
    skip_unit_test()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    skip_unit_test()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    skip_unit_test()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestRandomness"]["requestId"]
    # Mocking ChainLink Response
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )

    # account or player(0) should be the winner because: 777 % 3 = 0
    assert lottery.recent_winner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery

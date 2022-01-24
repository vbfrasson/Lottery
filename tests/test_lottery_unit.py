# 0.02 eth
# 200_000_000_000
from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import *
from scripts.helpful_scripts import *
from web3 import Web3
import pytest

# Unit tests - way to test small pieces of code in an isolated instance (local env)
# Integration tests - testing accross multiple complex systems (testnet)
def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    # Assert
    assert expected_entrance_fee == entrance_fee

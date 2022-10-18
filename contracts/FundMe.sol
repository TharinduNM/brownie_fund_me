// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    address public owner;
    address[] public funders;
    AggregatorV3Interface priceFeed;

    constructor(address _priceFeedAddress) {
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
        owner = msg.sender;
    }

    mapping(address => uint256) public addressOfFunder;

    function getEntryFee() public view returns (uint256) {
        uint256 minLimit = 5 * 10**18;
        uint256 precision = 1 * 10**18;
        uint256 price = getUSDPriceOfEth();
        return ((minLimit * precision) / price);
    }

    function fund() public payable {
        //50$ min fund limit
        uint256 minLimit = 5 * 10**18;
        require(getValueOfEth(msg.value) >= minLimit, "Spend more Loser!");
        addressOfFunder[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    //Goerli testnet ETH/USD pair
    function getUSDPriceOfEth() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        //in 18 digits
        return uint256(answer * 10**10);
    }

    function getValueOfEth(uint256 _ethAmount) public view returns (uint256) {
        uint256 ethValue = (_ethAmount * getUSDPriceOfEth()) /
            1000000000000000000;
        return ethValue;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressOfFunder[funder] = 0;
        }

        funders = new address[](0);
    }
}

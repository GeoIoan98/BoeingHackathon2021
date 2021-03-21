// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.1;
pragma abicoder v2;
pragma experimental SMTChecker;

contract oceanCoin {

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event NewBid(address indexed bidder, uint256 value);

    // ERC-20 variables
    string public name;
    string public symbol;
    uint public totalSupply;
    address public burnAddr = address(0x000000000000000000000000000000000000dEaD);
    mapping (address => uint) public balances;
    mapping (address => mapping (address => uint)) public allowed;

    // Volunteer network variables
    address public owner;
    address[] public organisations;
    struct orgDet {
        string name;
        string location;
        string email;
    }
    mapping (address => orgDet) public orgDetails;
    address[] public volunteers;
    struct volDet {
        string name;
    }
    mapping (address => orgDet) public volDetails;

    // Auction variables
    struct auctDet {
        uint bestBid;
        address highestBidder;
        uint expiration;
        bool status;
    }
    mapping (uint => auctDet) public auctions;
    uint public auctionCount;

    // Fallback, Constructor
    fallback () external {
        revert();
    }

    constructor() {
        // ERC-20
        totalSupply = 100; //Equal to the kilos of trash in the ocean
        balances[msg.sender] = 100;
        name = "Ocean Coin";
        symbol = "OCN";

        // Volunteer network
        owner = msg.sender;
        auctionCount = 0;
    }

    // ERC-20 Functions
    function transfer(address to, uint value) external returns (bool success) {
        if (balances[msg.sender] >= value && value > 0) {
            balances[msg.sender] -= value;
            balances[to] += value;
            emit Transfer(msg.sender, to, value);
            return true;
        }
        else {
            return false;
        }
    }

    function transferFrom(address from, address to, uint value) external returns (bool success) {
        if (balances[from] >= value && allowed[from][msg.sender] >= value && value > 0) {
            balances[to] += value;
            balances[from] -= value;
            allowed[from][msg.sender] -= value;
            emit Transfer(from, to, value);
            return true;
        }
        else {
            return false;
        }
    }

    function burn(uint value) external returns (bool success) {
        if (balances[msg.sender] >= value && value > 0) {
            balances[msg.sender] -= value;
            balances[burnAddr] += value;
            emit Burn(msg.sender, value);
            return true;
        }
        else {
            return false;
        }
    }

    function approve(address spender, uint value) external returns (bool success) {
        allowed[msg.sender][spender] = value;
        Approval(msg.sender, spender, value);
        return true;
    }

    // Volunteer network
    function addOrganisation(address addr, string memory orgName, string memory location, string memory email) external {
        require(msg.sender == owner);
        organisations.push(addr);
        orgDetails[addr].name = orgName;
        orgDetails[addr].location = location;
        orgDetails[addr].email = email;
    }

    function addVolunteer(address addr, string memory name) external {
        bool found = false;
        if (owner == msg.sender) { found = true; }
        for (uint i = 0; i < organisations.length; i++) {
            if (organisations[i] == msg.sender) {
                found = true;
                break;
            }
        }
        if (found) {
            volunteers.push(addr);
            volDetails[addr].name = name;
        }
    }

    // Auction
    function startAuction(uint duration) external {
        auctions[auctionCount].highestBidder = address(0x0);
        auctions[auctionCount].bestBid = 0;
        auctions[auctionCount].expiration = block.number + duration;
        auctions[auctionCount].status = true;
        auctionCount++;
    }

    function bid(uint auctionId, uint value) external returns (uint best) {
        require(auctionId <= auctionCount);
        require(auctions[auctionId].status == true);
        require(balances[msg.sender] >= value && value > 0);
        require(value > auctions[auctionId].bestBid);
        balances[msg.sender] -= value;
        balances[auctions[auctionId].highestBidder] += auctions[auctionId].bestBid;
        auctions[auctionId].highestBidder = msg.sender;
        auctions[auctionId].bestBid = value;
        return value;
    }

    function endAuction(uint auctionId) external {
        require(auctionId <= auctionCount);
        require(auctions[auctionId].expiration <= block.number);
        auctions[auctionId].status = false;
    }
}

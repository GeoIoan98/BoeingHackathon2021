pragma solidity ^0.4.24;

contract Competition {

    struct Restaurant {
        address addr;
        string name;
        uint256 amount;
        uint256 expiration;
        address winner;
        Customer[] customers;
        uint256 length;
    }

    struct Customer {
        address addr;
        string name;
    }

    mapping (address => Restaurant) public restaurants;
    mapping (uint256 => Customer) public customers;
    mapping (address => address) public winners;

    address public owner;

    event informWinner(address winner);

    constructor() public {
        owner = msg.sender;
    }

    function add_restaurant_to_competition(string name, uint256 expiration) public payable {
        require(restaurants[msg.sender].addr == 0); // to ensure not again in competition
        Restaurant restaurant;
        restaurant.addr = msg.sender;
        restaurant.name = name;
        restaurant.amount = msg.value;
        restaurant.expiration = now + expiration;
        restaurant.length = 0;
        restaurants[msg.sender] = restaurant;
    }

    function add_customer_to_competition(string name, address restaurant, bytes32 hash, bytes signature) public {
        require(restaurants[msg.sender].addr == 0); // customer is not a restaurant
        require(now < restaurants[restaurant].expiration); // check that it is within the given period
        for (uint256 i = 0; i < restaurants[restaurant].length; i += 1) {
            require(restaurants[restaurant].customers[i].addr != msg.sender); // First time I am added to the competition, checks against replay attack
        }
        require(recover(hash, signature) == restaurant); // verify the signature

        Customer customer;
        customer.addr = msg.sender;
        customer.name = name;

        restaurants[restaurant].customers.push(customer);
        restaurants[restaurant].length += 1;
    }

    function get_winner(address restaurant) public {
        require(restaurants[restaurant].expiration <= now);
        require(restaurants[restaurant].winner == 0);
        uint256 length = restaurants[restaurant].length;
        uint randomnumber = uint(keccak256(abi.encodePacked(now, block.timestamp))) % length;
        restaurants[restaurant].winner = restaurants[restaurant].customers[randomnumber].addr;
        winners[restaurant] = restaurants[restaurant].customers[randomnumber].addr;
        emit informWinner(winners[restaurant]);

        restaurants[restaurant].winner.transfer(restaurants[restaurant].amount);
    }

    function show_winner(address restaurant) view public returns(address) {
        return winners[restaurant];
    }

    function recover(bytes32 hash, bytes signature) public pure returns(address) {
        bytes32 r;
        bytes32 s;
        uint8 v;

        assembly {
            r := mload(add(signature, 0x20))
            s := mload(add(signature, 0x40))
            v := byte(0, mload(add(signature, 0x60)))
        }

        if (v < 27) {
            v += 27;
        }

        if (v != 27 && v != 28) {
            return(address(0));
        }
        else {
            return ecrecover(hash, v, r, s);
        }
    }




}

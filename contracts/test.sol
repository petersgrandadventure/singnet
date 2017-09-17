pragma solidity ^0.4.11;

import "./ownership/ownable.sol";

contract Escrow is ownable {

    address public beneficiary;
}

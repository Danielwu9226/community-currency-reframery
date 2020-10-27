pragma solidity >=0.4.22 <0.8.0;

import '@openzeppelin/contracts/token/ERC20/ERC20.sol';

contract DANC is ERC20{
    constructor(address owner_address) ERC20("DANC COIN", "DNC") public{
    }
} 
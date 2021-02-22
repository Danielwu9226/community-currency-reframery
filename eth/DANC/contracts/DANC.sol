pragma solidity >=0.4.22 <0.8.0;

import '@openzeppelin/contracts/token/ERC20/ERC20.sol';

contract DANC is ERC20{
    constructor() ERC20("DANC TOKEN", "DANC") public{
    }
    function mint(uint256 amount) public {
        _mint(msg.sender, amount);
    }
} 

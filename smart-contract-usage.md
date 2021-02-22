# Introduction
Our community currency is implemented as a fungible token that can be exchanged between users on the Ethereum blockchain. Interactions with our smart contract will be abstracted by MetaMask and the frontend currently in development by the Aquafina team. 

This document will teach you how to test our smart contract using MetaMask and MEW. Our smart contract is currently deployed on the Ropsten test network so no real money will be needed for this test. 


# Setup 
### 1. MetaMask 
Metamask is a wallet for your browser. It's used by Dapps to interact with the blockchain using your Ethereum account credentials. We will be generating an Ethereum account and saving it in metamask. 
1. Download the metamask chrome extension: https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn?hl=en
2. Go through metamask setup to create a wallet.
3. Our ethereum smart contract currently lives on the Ropsten test network for prototyping. Switch the network from Ethereum mainnet to Ropsten Test Network. 

![switch-network.png](/readme-assets/switch-network.png?raw=true "switch-network")

4. Request free ethereum on the Ropsten test net. Copy your account address. 

![copy-address.png](/readme-assets/copy-address.png?raw=true "copy-address") 

Paste your account address [here](https://faucet.ropsten.be) and hit "Send me test Ether". You should see your account balance change to 1 ETH in a few seconds.

### 2. MEW
We will use MEW to interact with our smart contract deployed on the Ropsten network. 
1. Head to https://www.myetherwallet.com/access-my-wallet and select MEW CX ![mew1.png](/readme-assets/mew1.png)
2. Give MEW permission to access MetaMask and select your Ethereum account. ![mew2.png](/readme-assets/mew2.png)


# Usage
### Interact with smart contract via MEW
Once you have given MEW access to your Ethereum account, navigate to the contract section and paste in the contract address and contract ABI. The contract address is ```0x45BcC95Ca4EEC94755EB0B4B330D48D70D4a5142``` and the ABI can be found [here](/readme-assets/ABI.txt). 
Hit continue.

![mew3.png](/readme-assets/mew3.png)


You will be presented with a list of public functions provided by our smart contract. 

![mew4.png](/readme-assets/mew4.png)

Our smart contract imports the ERC20 token [implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol) provided by https://openzeppelin.com. There are a few functions that comes from openzeppelin which we do not plan on using for our application but is still displayed on MEW nonetheless. Testing will only be conducted on the functions that we will utilize in our application: balanceOf, totalSupply, transfer, mint. 

#### totalSupply
This function will return the total number of DANC coins in supply. Simply select totalSupply from the functions menu to see the total supply,. The total supply is displayed under Result. 
![mew-totalsupply.png](/readme-assets/mew-totalsupply.png)

#### balanceOf
This function will return the amount of DANC coins owned by an address. You can give it your own address from MetaMask and hit read. It should return zero for you as you have not received any DANC coins at this point.
![mew-balanceof.png](/readme-assets/mew-balanceof.png)

#### mint
*Right now, to allow testing like this, anyone can access this function and generate as many DANC coins as they want. In the future, this function will be restricted to admin accounts only.*

This function generates new coins for your account. Enter the number of coins you want to generate and hit write.
![mew-mint1.png](/readme-assets/mew-mint1.png)

Since this is a write function, a transaction signed by your Ethereum account will be sent to the blockchain network. Transactions require you to pay a transaction fee (gas fee) in ether. This is calculated automatically by MetaMask. Don't worry, you will be spending the free Ropsten test ether you received earlier in the MetaMask setup section.  
![mew-mint2.png](/readme-assets/mew-mint2.png)

After you hit confirm, it should take less than a minute for your account to receive the newly generated DANC coins. You can check the block confirmation progress by viewing your transaction on Etherscan.
1. Open MetaMask and click on most recent activity

![mew-mint3.png](/readme-assets/mew-mint3.png)

2. Open transaction on Etherscan

![mew-mint4.png](/readme-assets/mew-mint4.png)

![mew-mint5.png](/readme-assets/mew-mint5.png)

Go back to MEW and check the balanceOf your account and totalSupply again, they should be updated to reflect the new DANC coins generated. 

#### transferToken
The function allows you to transfer DANC coins from your Ethereum account to another Ethereum account. To test out this function, create another MetaMask account, copy the address of that account and then switch back to your original account. 

![mew-transferToken1.png](/readme-assets/mew-transferToken1.png)

On MEW, paste in the address of the new account into the Recipient textbox and enter the number of DANC coins you want to send. (Note: you won't be able to send more than what you have in your account) 

![mew-transferToken2.png](/readme-assets/mew-transferToken2.png)

Like mint, this is a write function so you can track your transaction on Etherscan. The balanceOf the new account address should reflect the number of coins transferred. 
Since mint and transferToken are write functions that require paying gas fees, you will need to load Ether into your new account to call those functions. You can follow the same steps from setup to request for free test ether from the [Ropsten faucet](https://faucet.ropsten.be). 


# Terminology
Fungible token: https://medium.com/0xcert/fungible-vs-non-fungible-tokens-on-the-blockchain-ab4b12e0181a

Smart contract: https://ethereum.org/en/developers/docs/smart-contracts/

ABI: https://docs.soliditylang.org/en/v0.5.3/abi-spec.html#:~:text=The%20Contract%20Application%20Binary%20Interface,as%20described%20in%20this%20specification

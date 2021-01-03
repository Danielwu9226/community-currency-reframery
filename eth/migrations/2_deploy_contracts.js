var DANC = artifacts.require("./DANC.sol");
module.exports = function (deployer) {
  deployer.deploy(DANC, '0x6da92759a555B745652ebF001cF3F5E7617B6Bb2');
};
var DANC = artifacts.require("./DANC.sol");
module.exports = function (deployer) {
  deployer.deploy(DANC, '0x8e0F25dFf03eFD12179181800082b2F60b10ce83');
};
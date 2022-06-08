// SPDX-License-Identifier: MIT
pragma solidity >=0.4.21 <0.9.0;

import "./TradeData.sol";

contract PerformanceTracker{

  constructor(){}

  // Track record to all (user, account) key-value pairs
  mapping(address => TradeData[]) trackRecords;
  address[] allUsers;

  function currentBlockTime() public view returns (uint256) {
      return block.timestamp;
  }

 function registerUser(address _blockchainAddress) public returns (address){

    // msg sender check ??

    // Check if user already exists,
    // if it does, revert to previous state
    if (isUserRegistered(_blockchainAddress)) {
      revert("User already exists");
    }

    // We add it to the dict/mapping of registered users
    TradeData[] memory someHash;
    trackRecords[_blockchainAddress] = someHash;

    // Insert into all users list
    allUsers.push(_blockchainAddress);

    // Emit event to signal registration of new user
    // emit();

    return _blockchainAddress;
  }

  function isUserRegistered(address _blockchainAddress) public view returns(bool){
    for (uint i=0; i < allUsers.length; i++) {
      if (_blockchainAddress == allUsers[i]) {
        return true;
        }
    }
    return false;
  }

 function getRegisteredUsersAddressList() public view returns (address[] memory)  {
     return allUsers;
 }


 function getTotalRegisteredUsers() public view returns (uint256) {
     return allUsers.length;
 }

 function getTotalNumberOfTradeHashes() public view returns (uint256) {

   uint totalTradeHashes = 0;

    for(uint i=0; i < allUsers.length; i++){
      address some_address = allUsers[i];
      totalTradeHashes += trackRecords[some_address].length;
    }
    return totalTradeHashes;
 }


  //record trades onto blockchain
  function recordTrade(address _blockchainAddress, uint timestamp, string memory hash_) public returns (address){

    // Check if user already exists,
    // if it does, revert to previous state
    if (!isUserRegistered(_blockchainAddress)) {
      revert("User not registered");
    }

    // We add it to the dict/mapping of registered users
    // = new TradeData(timestamp, hash_);
    trackRecords[_blockchainAddress].push(new TradeData(timestamp, hash_));

    // Insert into all users list
    // allUsers.push(_blockchainAddress);

    // Emit event to signal registration of new user
    // emit();

    return _blockchainAddress;
  }


}
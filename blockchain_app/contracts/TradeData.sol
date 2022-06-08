// SPDX-License-Identifier: MIT
pragma solidity >=0.4.21 <0.9.0;

contract TradeData {

    string someHash;
    uint timestamp;

    constructor(uint _ts, string memory _hs) {
        timestamp = _ts;
        someHash = _hs;
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract BlockTRX {
    mapping(string => address) private s_cidToAddress;
    mapping(string => string) private s_cidToResult;

    function setCidToAddress(address user, string memory cid) external {
        require(
            s_cidToAddress[cid] == address(0),
            "Address for this CID already exists"
        );
        s_cidToAddress[cid] = user;
    }

    function getCidToAddress(
        string memory cid
    ) external view returns (address) {
        return s_cidToAddress[cid];
    }

    function setCidToResult(string memory cid, string memory result) external {
        require(
            bytes(s_cidToResult[cid]).length == 0,
            "Result for this CID already exists"
        );
        s_cidToResult[cid] = result;
    }

    function getCidToResult(
        string memory cid
    ) external view returns (string memory) {
        return s_cidToResult[cid];
    }
}

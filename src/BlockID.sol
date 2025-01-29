// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract BlockID {
    mapping(address => string) private s_blockId;

    event BlockIdSet(address indexed user, string blockId);

    function setBlockId(address user, string calldata blockId) external {
        s_blockId[user] = blockId;
        emit BlockIdSet(user, blockId);
    }

    function getBlockId(address user) external view returns (string memory) {
        return s_blockId[user];
    }
}

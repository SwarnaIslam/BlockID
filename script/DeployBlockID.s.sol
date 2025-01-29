// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import {Script} from "forge-std/Script.sol";
import {BlockID} from "../src/BlockID.sol";

contract DeployBlockID is Script {
    function run() external returns (BlockID) {
        vm.startBroadcast();
        BlockID blockID = new BlockID();
        vm.stopBroadcast();
        return blockID;
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import {Script} from "forge-std/Script.sol";
import {BlockTRX} from "../src/BlockTRX.sol";

contract DeployBlockTRX is Script {
    function run() external returns (BlockTRX) {
        vm.startBroadcast();
        BlockTRX blockTRX = new BlockTRX();
        vm.stopBroadcast();
        return blockTRX;
    }
}

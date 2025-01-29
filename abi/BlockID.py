blockABI = [
    {
      "type": "function",
      "name": "getBlockId",
      "inputs": [
        { "name": "user", "type": "address", "internalType": "address" }
      ],
      "outputs": [{ "name": "", "type": "string", "internalType": "string" }],
      "stateMutability": "view"
    },
    {
      "type": "function",
      "name": "setBlockId",
      "inputs": [
        { "name": "user", "type": "address", "internalType": "address" },
        { "name": "blockId", "type": "string", "internalType": "string" }
      ],
      "outputs": [],
      "stateMutability": "nonpayable"
    },
    {
      "type": "event",
      "name": "BlockIdSet",
      "inputs": [
        {
          "name": "user",
          "type": "address",
          "indexed": True,
          "internalType": "address"
        },
        {
          "name": "blockId",
          "type": "string",
          "indexed": False,
          "internalType": "string"
        }
      ],
      "anonymous": False
    }
]